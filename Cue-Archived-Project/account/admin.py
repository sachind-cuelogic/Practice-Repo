from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _

from account.models import UserProfile
from ppiauth.models import PPIUser
from ppiauth.forms import PPIUserChangeForm, PPIUserCreationForm


class UserInline(admin.StackedInline):
    """
    This class displays UserProfile inline with User.
    """
    model = UserProfile
    can_delete = False


class PPIUserAdmin(UserAdmin):
    form = PPIUserChangeForm
    add_form = PPIUserCreationForm

    list_display = ('email', 'is_active')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('personal info', {
            'fields': ('date_joined', 'activation_key', 'key_expires')
        }),
        ('permissions', {'fields': ('is_active', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password', 'password_repeat')}),)
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined',)
    filter_horizontal = ()
    inlines = (UserInline, )


admin.site.register(PPIUser, PPIUserAdmin)
