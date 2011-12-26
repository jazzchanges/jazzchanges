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
from jazzchanges.tunes.forms import TuneForm

def root(request):
    tunes = Tune.objects.all()
    return render_to_response('directory/root.html', RequestContext(request, locals()))

def view_tune(request, tune_id, artist_slug, title_slug, key=None, template='directory/view.html'):
    tunes = Tune.objects.all()
    tune = get_object_or_404(Tune, id=tune_id)

    # do redirect if url slugs are off
    if artist_slug != tune.artist_slug or title_slug != tune.title_slug:
        if key:
            return HttpResponseRedirect(reverse('directory:view_key', args=[tune.id, tune.artist_slug, tune.title_slug, key]))
        return HttpResponseRedirect(reverse('directory:view', args=[tune.id, tune.artist_slug, tune.title_slug]))

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

def view_tune_fullscreen(*args, **kwargs):
    kwargs['template'] = 'directory/fullscreen.html'
    return view_tune(*args, **kwargs)