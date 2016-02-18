from django.contrib import admin

from eventex.core.models import Speaker, Contact, Talk, Course


class ContactInline(admin.TabularInline):

    model = Contact
    extra = 1


class SpeakerModelAdmin(admin.ModelAdmin):

    inlines = [ContactInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'website_link', 'thumb', 'email', 'phone']

    def website_link(self, obj):
        return '<a href="{0}">{0}</a>'.format(obj.website)

    website_link.allow_tags = True
    website_link.short_description = 'website'

    def thumb(self, obj):
        return '<img width="48px" src="{}" />'.format(obj.photo)

    thumb.allow_tags = True
    thumb.short_description = 'foto'

    def email(self, obj):
        addr = obj.contact_set.emails().first()
        if not addr:
            return None
        return '<a href="mailto:{addr}">{addr}</a>'.format(addr=addr)

    email.allow_tags = True
    email.short_description = 'e-mail'

    def phone(self, obj):
        return obj.contact_set.phones().first()

    phone.short_description = 'telefone'


class TalkModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(course=None)


admin.site.register(Speaker, SpeakerModelAdmin)
admin.site.register(Talk, TalkModelAdmin)
admin.site.register(Course)
