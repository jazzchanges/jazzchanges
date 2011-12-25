from django.contrib import admin

from jazzchanges.tunes.models import Tune, Change



class ChangeAdmin(admin.ModelAdmin): 
    list_display = [f.name for f in Change._meta.fields]
admin.site.register(Change, ChangeAdmin)


class ChangeInline(admin.TabularInline):
    model = Change

class TuneAdmin(admin.ModelAdmin): 
    list_display = [f.name for f in Tune._meta.fields]
    
    inlines = [
        ChangeInline
    ]
admin.site.register(Tune, TuneAdmin)