from jazzchanges import settings

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms.models import model_to_dict

from django.forms.models import modelformset_factory

from jazzchanges.tunes.models import Tune, Change, KEYS, KEY_DICT
from jazzchanges.tunes.forms import TuneForm, EditTuneForm, RawEditTuneForm, build_changeform

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
def view_tune_fullscreen(*args, **kwargs):
    kwargs['template'] = 'tunes/fullscreen.html'
    return view_tune(*args, **kwargs)

@login_required
def edit_tune(request, tune_id):
    tune = get_object_or_404(Tune, owner=request.user, id=tune_id)
    changes = tune.changes.select_related().all()

    ChangeForm = build_changeform(tune)
    extra = 0 if len(changes) else 1
    ChangeFormSet = modelformset_factory(Change, form=ChangeForm, can_delete=True, extra=extra)

    if request.method == 'POST':
        formset = ChangeFormSet(request.POST, queryset=changes, prefix='changes')

        if formset.is_valid():
            instances = formset.save(commit=False)

            for i, change in enumerate(instances):
                change.tune = tune
                #change.order = i

                change.save()

            messages.success(request, 'Tune changes saved.')
            return HttpResponseRedirect(reverse('tunes:view', args=[tune.id]))
    else:
        formset = ChangeFormSet(queryset=changes, prefix='changes')
    
    return render_to_response('tunes/edit.html', RequestContext(request, locals()))

@login_required
def edit_tune_raw(request, tune_id):
    tune = get_object_or_404(Tune, owner=request.user, id=tune_id)

    if request.method == 'POST':
        form = RawEditTuneForm(request.POST, request.FILES)

        if form.is_valid():
            tune.changes.all().delete()
            tune.load(form.cleaned_data['raw'], save=True)
            messages.success(request, 'Tune saved.')
            return HttpResponseRedirect(reverse('tunes:view', args=[tune.id]))
    else:
        form = RawEditTuneForm(
            initial={'raw': tune.dump()})
    
    return render_to_response('tunes/edit_meta.html', RequestContext(request, locals()))

@login_required
def edit_tune_meta(request, tune_id):
    tune = get_object_or_404(Tune, owner=request.user, id=tune_id)

    if request.method == 'POST':
        form = EditTuneForm(request.POST, request.FILES)

        if form.is_valid():
            [setattr(tune, k, v) for k, v in form.cleaned_data.items()]
            tune.save()
            messages.success(request, 'Tune saved.')
            return HttpResponseRedirect(reverse('tunes:view', args=[tune.id]))
    else:
        form = EditTuneForm(
            initial=model_to_dict(tune, 
                fields=['title', 'artist', 'key', 'time']))
    
    return render_to_response('tunes/edit_meta.html', RequestContext(request, locals()))

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