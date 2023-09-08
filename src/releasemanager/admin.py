from django.contrib import admin

# from .models import ReleaseGroup, Release, Package
from .models import Release, Package, ReleaseGroup


# Inlines


class ReleaseInline(admin.TabularInline):
    # You can use admin.StackedInline for a different display style
    model = Release
    extra = 1  # Number of empty forms to display for adding new releases


# Admins


class ReleaseGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    filter_horizontal = ("members",)


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("package", "version", "release_date", "active")
    search_fields = ("package__name", "version")


class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    # prepopulated_fields = {"name": ("name",)}
    inlines = [ReleaseInline]


admin.site.register(ReleaseGroup, ReleaseGroupAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Package, PackageAdmin)
