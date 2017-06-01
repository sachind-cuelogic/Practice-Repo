from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import ugettext as _
from core.models import HomePageConfig
from core.forms import HomePageConfigForm

class HomePageConfigAdmin(admin.ModelAdmin):
    form = HomePageConfigForm
    list_display = ('display_message', 'active',)
    readonly_fields = ('created_at',)

class AdminSite(AdminSite):
    site_title = _('Pre-Pair It site')
    site_header = _('Pre-Pair It administration')
    index_title = _('Pre-Pair It Site administration')

admin.site = AdminSite()
admin.site.register(HomePageConfig,HomePageConfigAdmin)
