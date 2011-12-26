$(document).ready(function() {

  $('.alert-message .ignore').click(function() {
    $(this).closest('.alert-message').slideUp();
  });

  $('.dropdown').dropdown();

  $('form.changes .field-delete-button as').on('click', function() {
    $(this).closest('.change').find('.field-DELETE input').attr('checked', 'checked').val('on');
    $(this).closest('.change').slideUp();
  });

  function addFormset(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    newElement.find(':input').each(function() {
      var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
      var id = 'id_' + name;

      if ($(this).attr('type') != 'hidden') {
        $(this).val('');
      }
      
      $(this).attr({'name': name, 'id': id}).removeAttr('checked');
    });

    newElement.find('label').each(function() {
      var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
      $(this).attr('for', newFor);
    });

    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).after(newElement);
  }

  function deleteFormset(element, type) {
    if ($("form.changes .changes-inner .change").size() < 2) { return false; };

    element = $(element);

    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    element.remove();
    total--;
    $('#id_' + type + '-TOTAL_FORMS').val(total);

    return false;

    // extra when we used to do this with ajax
    // to go back to doing it this way, make sure
    // you make the view return something besides
    // a httpresponseredirect
    if (element.find('[type="hidden"]').val()) {
    var ps_id = element.find('[type="hidden"]').val();
    $.ajax({
      url: '{% url checkout %}', // delete from cart
      data: { id: ps_id },
      success: function() {
        element.remove();
        total--;
        $('#id_' + type + '-TOTAL_FORMS').val(total);
      }
      })
    } else {

    };
  }

  function renumberFormset() {
    $('form.changes .changes-inner .change').each(function(index, element){
      $(element).find('input, select').each(function(inner_index, inner_element){
        //alert($(this).attr('name'));
        //alert($(this).attr('name').replace(/[\d\.]+/g, index));
        $(this).attr('name', $(this).attr('name').replace(/[\d\.]+/g, index) );
        $(this).attr('id', $(this).attr('id').replace(/[\d\.]+/g, index) );
      });

      $(element).find('label').each(function(inner_index, inner_element){
        $(this).attr('for', $(this).attr('for').replace(/[\d\.]+/g, index) );
      });

      $(element).find('.field-order input').val(index); // only on filled ones
    });
  }

  $("a.add-form").on('click', function() {
    addFormset('form.changes .changes-inner .change:last', 'changes');

    renumberFormset();
  })

  $('form.changes .field-delete-button a').on('click', function() {
    var form = $(this).closest('.change');

    if (form.find('input[type=hidden]').val()) {
      // this is a pre existing change
      form.find('.field-DELETE input').attr('checked', 'checked').val('on');
      form.slideUp();
    } else {
      // a blank form is deleted
      deleteFormset(form, 'changes');
    }

    renumberFormset();
  })

  $('.changes-inner').sortable({
    stop: function(event, ui) {
      renumberFormset();
    }
  });

  renumberFormset();
});