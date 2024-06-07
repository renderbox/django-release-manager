from django.contrib import admin

from .models import Release

# Inlines

# Admins


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("package", "name", "release_date", "active")
    search_fields = ("package__name", "name")


admin.site.register(Release, ReleaseAdmin)
