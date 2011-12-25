$(document).ready(function() {

  $('.alert-message .ignore').click(function() {
    $(this).closest('.alert-message').slideUp();
  });

  $('.dropdown').dropdown();
});