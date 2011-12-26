from django import forms

from bootstrap.forms import BootstrapForm, Fieldset

from jazzchanges.tunes.models import KEYS, TIMES

class TuneForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset('New Tune', 'title', 'key', 'time'),
        )
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class':'xlarge'}))
    
    key = forms.IntegerField(
        label='Original Key',
        help_text="Don't worry about major or minor, we don't track that.",
        min_value=1,
        max_value=12,
        widget=forms.Select(choices=KEYS, attrs={'class':'small'}))
    
    time = forms.CharField(
        label='Time Signature',
        initial='4/4',
        widget=forms.Select(choices=TIMES, attrs={'class':'small'}))