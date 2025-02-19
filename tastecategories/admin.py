from django.contrib import admin

from tastecategories.models import TasteCategories


@admin.register(TasteCategories)
class TasteCategoriesAdmin(admin.ModelAdmin):
    list_display = ['name']
