from django.contrib import admin

# Register your models here.

from .models import Workshop, Entrie, Day


class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('date', 'teachers', 'time')


class DayEntrieInline(admin.StackedInline):
    model = Entrie
    extra = 1
    can_delete = True
    show_can_change = True


class DayAdmin(admin.ModelAdmin):
    inlines = [
        DayEntrieInline,
    ]


admin.site.register(Day, DayAdmin)
admin.site.register(Workshop, WorkshopAdmin)
