from django import forms

from bootstrap.forms import BootstrapForm, Fieldset

from jazzchanges.tunes.models import KEYS

class TuneForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset('New Tune', 'title', 'key'),
        )
    
    title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class':'xlarge'}))
    
    key = forms.IntegerField(   
        min_value=1,
        max_value=12,
        widget=forms.Select(choices=KEYS, attrs={'class':'small'}))