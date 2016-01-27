from django.contrib import admin

from eventex.core.models import Speaker


class SpeakerModelAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'website_link', 'thumb']

    def website_link(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.website)

    website_link.allow_tags = True
    website_link.short_description = 'website'

    def thumb(self, obj):
        return '<img width="48px" src="{}" />'.format(obj.photo)

    thumb.allow_tags = True
    thumb.short_description = 'foto'

admin.site.register(Speaker, SpeakerModelAdmin)
