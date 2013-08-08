from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from . import models, forms
import common.admin as ca

class AccountAdmin(UserAdmin):
    # The forms to add and change user instances
    form = forms.AccountChangeAdminForm
    add_form = forms.AccountCreationAdminForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(models.Account, AccountAdmin)
# ... and, since we're not using Django's builtin permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class AuthorAdmin(ca.MyModelAdmin):
    add_form = forms.AuthorCreationForm
    form = forms.AuthorForm
    fieldsets = []
    list_display = ('name',)
    inlines = [ca.ImageInline,]

admin.site.register(models.Author, AuthorAdmin)
