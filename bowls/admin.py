from django.contrib import admin
from django.utils.safestring import mark_safe

from bowls.models import Bowls


@admin.register(Bowls)
class BowlsAdmin(admin.ModelAdmin):
    change_form_template = 'admin/bowls/change_form.html'
    list_display = ['type', 'description', 'howTo', 'image_preview']
    search_fields = ['type']

    def image_preview(self, obj):
        try:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        except ValueError:
            return mark_safe(f'<img src="/media/placeholder.jpg" width="100" />')

    image_preview.short_description = 'Image Preview'
