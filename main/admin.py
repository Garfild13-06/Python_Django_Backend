from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


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
