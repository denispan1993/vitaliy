# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import Permission
from django.contrib.auth.admin import GroupAdmin #  as DjangoGroupAdmin

from .models import User, Email, Phone

__author__ = 'AlexStarov'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, )
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, )

    class Meta:
        model = User
        fields = ('username', )  # 'date_of_birth', 'gender', 'phone',

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match", )
        return password2

    def save(self, commit=True, ):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self, ).save(commit=False, )
        user.set_password(self.cleaned_data["password1"], )
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm, ):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('password', 'is_active', )  # 'date_of_birth', 'is_admin',

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(DjangoUserAdmin, ):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('pk', 'username', 'first_name', 'last_name', 'patronymic', 'gender', 'date_of_birth',
                    'is_superuser', 'is_staff', 'is_active', )
    list_display_links = ('pk', 'username', 'first_name', 'last_name', 'patronymic', 'gender', 'date_of_birth', )
    list_filter = ('is_superuser', 'is_staff', 'is_active', )
    fieldsets = (
        (None, {'fields': ('username', 'password'), }, ),
        (_('Personal info', ), {'fields': ('first_name', 'last_name', 'patronymic',
                                           'gender', 'date_of_birth', ), }, ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions'), }, ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', ), }, ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'date_of_birth', 'password1', 'password2'), },
         ),
    )
    search_fields = ('username', 'first_name', 'last_name', 'patronymic', )
    ordering = ('id', 'username', )
    filter_horizontal = ('groups', 'user_permissions', )

# Now register the new UserAdmin...
admin.site.unregister(User, )
admin.site.register(User, UserAdmin, )
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group, )


class MyGroupAdmin(GroupAdmin, ):
    list_display = ('pk', 'name', )
    list_display_links = ('pk', 'name', )
    # list_filter = ('is_superuser', 'is_staff', 'is_active', )

# admin.site.unregister(GroupAdmin, )
admin.site.register(Group, MyGroupAdmin, )
#admin.site.register(Permission, )


class PermissionAdmin(admin.ModelAdmin, ):
    list_display = ('pk', 'name', 'content_type', 'codename', )
    list_display_links = ('pk', 'name', 'content_type', 'codename', )
    # list_filter = ('is_superuser', 'is_staff', 'is_active', )

## admin.site.unregister(Permission, )
admin.site.register(Permission, PermissionAdmin, )
#admin.site.register(Permission, )

#admin.site.unregister(ContentType, )
admin.site.register(ContentType, )


class EmailAdmin(admin.ModelAdmin, ):
    list_display = ('pk', 'user', 'email', 'test', 'created_at', 'updated_at', )
    list_display_links = ('pk', 'user', 'email', )
    search_fields = ['email', ]

admin.site.register(Email, EmailAdmin, )


class PhoneAdmin(admin.ModelAdmin, ):
    list_display = ('pk', 'user', 'phone', 'int_code', 'int_phone', 'primary', 'sms_notification', 'created_at', 'updated_at', )
    list_display_links = ('pk', 'user', 'phone', )
    search_fields = ['phone', 'int_code', 'int_phone', ]

admin.site.register(Phone, PhoneAdmin, )
