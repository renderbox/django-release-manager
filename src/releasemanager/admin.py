from django.contrib import admin

# from .models import ReleaseGroup, Release, Package
from .models import Release, Package, ReleaseState, ReleaseGroup


class ReleaseGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    filter_horizontal = ("members",)


class ReleaseStateAdmin(admin.ModelAdmin):
    list_display = ("name", "release_state_key", "description")


class ReleaseInline(admin.TabularInline):
    # You can use admin.StackedInline for a different display style
    model = Release
    extra = 1  # Number of empty forms to display for adding new releases


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("package", "version", "release_date", "state")
    # list_filter = ("package", "release_date")
    search_fields = ("package__name", "version")
    # filter_horizontal = ("groups",)


class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    # prepopulated_fields = {"name": ("name",)}
    inlines = [ReleaseInline]


admin.site.register(ReleaseGroup, ReleaseGroupAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(ReleaseState, ReleaseStateAdmin)
