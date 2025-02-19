from django.contrib import admin
from django.utils.safestring import mark_safe

from tobaccos.models import Tobaccos


@admin.register(Tobaccos)
class TobaccosAdmin(admin.ModelAdmin):
    change_form_template = 'admin/tobaccos/change_form.html'
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
