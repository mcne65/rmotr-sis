from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


class AccountsUserAdmin(UserAdmin):

    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'birth_date', 'twitter_handle',
                                         'github_handle', 'cloud9_handle',
                                         'timezone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined',
                                           'last_activity')}),
    )

admin.site.register(User, AccountsUserAdmin)
