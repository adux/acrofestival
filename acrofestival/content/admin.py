from django.contrib import admin
from django.utils.html import format_html

from acrofestival.content.models import (
    ContentSnippet,
    ContentSnippetHistory,
    Teacher,
    TeacherAppearance,
)
from acrofestival.content.snippets import ContentSnippets


class TeacherAppearanceInline(admin.TabularInline):
    model = TeacherAppearance
    extra = 0
    fields = ("festival_key", "year", "order", "is_published", "role_label")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "thumb", "appearance_count")
    search_fields = ("name", "country", "bio")
    inlines = [TeacherAppearanceInline]

    def thumb(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:40px;border-radius:4px">', obj.photo.url)
        return ""

    thumb.short_description = "photo"

    def appearance_count(self, obj):
        return obj.appearances.count()

    appearance_count.short_description = "appearances"


@admin.register(TeacherAppearance)
class TeacherAppearanceAdmin(admin.ModelAdmin):
    list_display = ("teacher", "festival_key", "year", "order", "is_published")
    list_filter = ("festival_key", "year", "is_published")
    search_fields = ("teacher__name",)
    autocomplete_fields = ("teacher",)


@admin.register(ContentSnippet)
class ContentSnippetAdmin(admin.ModelAdmin):
    list_display = ("key", "value_preview", "updated_at", "updated_by")
    search_fields = ("key", "value")
    readonly_fields = ("updated_at",)
    ordering = ("key",)

    def value_preview(self, obj):
        return (obj.value[:80] + "…") if len(obj.value) > 80 else obj.value

    value_preview.short_description = "value"

    def save_model(self, request, obj, form, change):
        if not obj.updated_by_id:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        ContentSnippetHistory.objects.create(
            key=obj.key,
            value=obj.value,
            edited_by=request.user,
            edited_by_name=request.user.get_full_name() or request.user.get_username(),
            note="edited via Django admin",
        )
        ContentSnippets.bump_version()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        ContentSnippets.bump_version()

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)
        ContentSnippets.bump_version()


@admin.register(ContentSnippetHistory)
class ContentSnippetHistoryAdmin(admin.ModelAdmin):
    list_display = ("key", "value_preview", "edited_at", "edited_by_name", "note")
    search_fields = ("key", "value", "edited_by_name")
    list_filter = ("edited_at",)
    readonly_fields = (
        "key",
        "value",
        "edited_at",
        "edited_by",
        "edited_by_name",
        "note",
    )
    ordering = ("-edited_at",)

    def value_preview(self, obj):
        return (obj.value[:80] + "…") if len(obj.value) > 80 else obj.value

    value_preview.short_description = "value"

    def has_add_permission(self, request):
        return False
