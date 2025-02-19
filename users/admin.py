from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe

from users.models import CustomUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'username', 'is_active', 'is_staff')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = UserCreationForm
    form = UserChangeForm

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password', 'avatar', 'nickname', 'is_active', 'is_staff', 'is_superuser',
                'groups',
                'user_permissions'),
        }),
    )

    # Поля для отображения и редактирования существующего пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('username', 'avatar', 'avatar_preview', 'nickname')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('email', 'username', 'nickname', 'is_staff', 'is_active', 'date_joined', 'avatar_preview')
    search_fields = ('email', 'username')
    ordering = ('email',)
    readonly_fields = ('date_joined', 'avatar_image', 'avatar_preview')

    def avatar_image(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="100" height="100" />')
        else:
            return mark_safe(f'<img src="/media/placeholder.jpg" width="100" />')

    def avatar_preview(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="100" height="100" />')
        else:
            return mark_safe('<img src="/media/placeholder.jpg" width="100" height="100" />')

    avatar_preview.short_description = 'Avatar Preview'
