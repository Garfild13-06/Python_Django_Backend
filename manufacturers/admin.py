from django.contrib import admin
from django.utils.safestring import mark_safe

from manufacturers.models import Manufacturers


# Register your models here.
@admin.register(Manufacturers)
class ManufacturersAdmin(admin.ModelAdmin):
    change_form_template = 'admin/manufacturers/change_form.html'
    list_display = ('name', 'description', 'image_preview')
    sortable_by = 'name'
    search_fields = ['name']

    def image_preview(self, obj):
        try:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        except ValueError:
            return mark_safe(f'<img src="/media/placeholder.jpg" width="100" />')

    image_preview.short_description = 'Image'
