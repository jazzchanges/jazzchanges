from django import forms

from bootstrap.forms import BootstrapForm, Fieldset

from jazzchanges.tunes.models import KEYS, TIMES


class TuneForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset('New Tune', 'title', 'artist', 'key', 'time'),
        )
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class':'xlarge'}))
    
    artist = forms.CharField(
        label='Original Artist',
        max_length=255,
        widget=forms.TextInput(attrs={'class':'xlarge'}))
    
    key = forms.IntegerField(
        label='Original Key',
        min_value=1,
        max_value=12,
        widget=forms.Select(choices=KEYS, attrs={'class':'small'}))
    
    time = forms.CharField(
        label='Time Signature',
        initial='4/4',
        widget=forms.Select(choices=TIMES, attrs={'class':'small'}))


class EditTuneForm(TuneForm):
    class Meta:
        layout = (
            Fieldset('Edit Metadata', 'title', 'artist', 'key', 'time'),
        )