from jazzchanges import settings

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms.models import model_to_dict

from jazzchanges.tunes.models import Tune, Change, KEYS, KEY_DICT
from jazzchanges.tunes.forms import TuneForm

@login_required
def workspace(request):
    return render_to_response('tunes/workspace.html', RequestContext(request, locals()))

@login_required
def new_tune(request):
    if request.method == 'POST':
        form = TuneForm(request.POST, request.FILES)

        if form.is_valid():
            tune = Tune(owner=request.user, **form.cleaned_data)
            tune.save()

            messages.success(request, 'Tune created.')
            return HttpResponseRedirect(reverse('tunes:view', args=[tune.id]))
    else:
        form = TuneForm()
    
    return render_to_response('tunes/new.html', RequestContext(request, locals()))

@login_required
def view_tune(request, tune_id, key=None, template='tunes/view.html'):
    tune = get_object_or_404(Tune, owner=request.user, id=tune_id)
    keys = KEYS

    if key:
        key = int(key)

        if 1 > key or key > 12:
            raise Http404

        systems = tune.get_systems(key=key)
    else:
        key = tune.key
        systems = tune.get_systems() # can pass in width=620
    
    letter_key = KEY_DICT[key]

    return render_to_response(template, RequestContext(request, locals()))

@login_required
def view_tune_fullscreen(request, tune_id, key=None):
    return view_tune(request, tune_id, key=key, template='tunes/fullscreen.html')

@login_required
def edit_tune(request, tune_id):
    tune = get_object_or_404(Tune, owner=request.user, id=tune_id)

    if request.method == 'POST':
        form = EditTune(request.POST, request.FILES)

        if form.is_valid():
            tune = Tune(owner=request.user, **form.cleaned_data)
            tune.save()

            messages.success(request, 'Product created.')
            return HttpResponseRedirect(reverse('tunes:edit', args=[tune.id]))
    else:
        form = EditTune()
    
    return render_to_response('tunes/edit.html', RequestContext(request, locals()))

@login_required
def delete_tune(request, tune_id):
    tune = get_object_or_404(Tune, owner=request.user, id=tune_id)

    if request.GET.get('confirm', 'no') == 'yes':
        tune.delete()
        messages.success(request, 'Tune deleted.')
        return HttpResponseRedirect(reverse('tunes:workspace'))
    else:
        # offer link to products:change_file + ?confirm=yes
        return render_to_response(
            'tunes/confirm_delete.html', 
            RequestContext(request, locals()))