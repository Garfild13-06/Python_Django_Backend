from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
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


class MixesAdminForm(forms.ModelForm):
    class Meta:
        model = Mixes
        fields = '__all__'

    def clean_categories(self):
        cats = self.cleaned_data['categories']
        if cats.count() != 2:
            raise ValidationError("Необходимо выбрать ровно 2 категории вкусов.")
        return cats


@admin.register(Mixes)
class MixesAdmin(admin.ModelAdmin):
    form = MixesAdminForm  # ПРИКРЕПИ новую форму
    change_form_template = 'admin/mixes/change_form.html'
    list_display = ["name", "description", "created", "banner_preview"]
    search_fields = ['name']
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
