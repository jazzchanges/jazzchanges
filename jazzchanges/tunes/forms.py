from django import forms

from bootstrap.forms import BootstrapForm, Fieldset

from jazzchanges.tunes.models import (  Change, KEYS, EXTENDED_KEY_DICT, 
                                        TIMES, INTERVALS, REVERSE_EXTENSIONS_DICT,
                                        REVERSE_KEY_DICT, REVERSE_INTERVAL_DICT)


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


class RawEditTuneForm(BootstrapForm):
    class Meta:
        layout = (
            Fieldset('Edit Tune', 'raw'),
        )
    
    raw = forms.CharField(
        label='Edit Raw',
        help_text='Do not use this if this confuses you!',
        widget=forms.Textarea(attrs={'class':'xlarge'}))


def build_changeform(tune):
    class ChangeForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(ChangeForm, self).__init__(*args, **kwargs)

            # replace the nasty old intervals with better 
            NEW_INTERVALS = [(x, tune.get_root(x)) for x, y in INTERVALS]

            self.fields['interval'].label = ''
            self.fields['interval'].choices = NEW_INTERVALS
            self.fields['bass'].choices = [('', '---')] + NEW_INTERVALS
            self.fields['beats'].widget.attrs['autocomplete'] = 'off'
        
        class Meta:
            model = Change
            fields = ('interval', 'extension', 'bass', 'beats', 'order')
    
    return ChangeForm