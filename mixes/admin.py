from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.utils.safestring import mark_safe

from tastecategories.models import TasteCategories
from mixes.models import MixTobacco, MixBowl, Mixes, MixLikes, MixFavorites


# Register your models here.
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
    change_form_template = 'admin/mixes/change_form.html'
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
