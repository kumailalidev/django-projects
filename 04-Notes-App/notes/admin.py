from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    exclude = [
        "slug",
    ]


admin.site.register(Tag, TagAdmin)
