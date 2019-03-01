from django.contrib import admin


# Register your models here.

from .models import Fest


class FestAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'name', 'email', 'numero', 'address', 'option', 'allergies', 'status',
                    'pay_till', 'pay_date', 'amount')
    list_filter = ('datetime', 'option', 'status')
    search_fields = ('name', 'email')


admin.site.register(Fest, FestAdmin)
