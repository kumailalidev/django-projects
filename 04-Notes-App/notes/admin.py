from typing import Any
from django.contrib import admin

from .models import Note, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    exclude = [
        "slug",
    ]


admin.site.register(Tag, TagAdmin)


class NoteAdmin(admin.ModelAdmin):
    # display tags related to note
    def tags_list(self, obj):
        tags = ", ".join([str(tag) for tag in obj.tags.all()])
        return tags if tags else "None"

    tags_list.short_description = "Related tags"

    list_display = (
        "title",
        "user",
        "status",
        "tags_list",
        "updated_at",
    )

    # override save_model method to automatically assign
    # currently logged-in admin as user
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
        return super().save_model(request, obj, form, change)


admin.site.register(Note, NoteAdmin)
