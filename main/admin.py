from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import BaseInlineFormSet
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from config import settings
from .models import *


class MyAdminSite(admin.AdminSite):
    site_header = 'inHookah admin panel'

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path('swagger/', self.admin_view(self.swagger_view))
        ]
        return custom_urls + urls

    def swagger_view(self, request):
        url = reverse('schema-swagger-ui')
        return format_html('<script>window.location="{}";</script>', url)


admin_site = MyAdminSite(name='myadmin')

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
            'fields': ('email', 'username', 'password', 'avatar', 'nickname', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
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



class MixTobaccoInline(admin.TabularInline):
    model = MixTobacco

# Инлайн для связи Микс-Чаша
class MixBowlInline(admin.StackedInline):
    model = MixBowl
    extra = 1  # Позволяет добавить одну чашу к миксу (можно изменить по желанию)

class MixAdminForm(forms.ModelForm):
    Categories = forms.ModelMultipleChoiceField(
        queryset=TasteCategories.objects.all(),
        required=False,
        widget=FilteredSelectMultiple("categories", is_stacked=False))

    class Meta:
        model = Mixes
        fields = ['name', 'description', 'banner', 'categories']


@admin.register(Mixes)
class MixesAdmin(admin.ModelAdmin):
    # Подключаем шаблон для отображения изображения в шапке
    change_form_template = 'admin/main/MixesModel/change_form.html'
    #  Подключаем форму MixAdminForm для изменения формы выбора категорий
    # form = MixAdminForm
    # Исключаем поле выбора категорий по-умолчанию
    # exclude = ["categories"]
    list_display = ["name", "description", "created", "banner_preview"]
    search_fields = ['name']
    # Подключаем форму выбора табаков
    inlines = [MixTobaccoInline, MixBowlInline]

    # Функция для добавления превью изображения в общем списке миксов
    def banner_preview(self, obj):
        # пробуем преобразовать в HTML-разметку с картинкой, иначе возвращаем заглушку
        try:
            return mark_safe(f'<img src="{obj.banner.url}" width="100" />')
        except ValueError:
            return mark_safe(f'<img src="/media/placeholder.jpg" width="100" />')

    banner_preview.short_description = 'banner'


@admin.register(MixLikes)
class MixLikesAdmin(admin.ModelAdmin):
    list_display = ["id", "mix", "user", "created"]


@admin.register(MixFavorites)
class MixFavoritesAdmin(admin.ModelAdmin):
    list_display = ["id", "mix", "user", "created"]


@admin.register(Tobaccos)
class TobaccosAdmin(admin.ModelAdmin):
    change_form_template = 'admin/main/TobaccosModel/change_form.html'
    list_display = ['taste',
                    'manufacturer',
                    'description',
                    # 'tobacco_leaf',
                    'tobacco_resistance',
                    'tobacco_strength',
                    # 'tobacco_slicing',
                    # 'tobacco_moisture',
                    'image_preview']
    search_fields = ['taste']

    def image_preview(self, obj):
        try:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        except ValueError:
            # return "No image"
            return mark_safe(f'<img src="/media/placeholder.jpg" width="100" />')

    image_preview.short_description = 'Image'

    list_filter = ['manufacturer']


@admin.register(TasteCategories)
class TasteCategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']
