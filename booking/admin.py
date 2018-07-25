from django.contrib import admin
from .models import Booking
# Register your models here.


class BookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'name', 'email', 'option', 'comment', 'status', 'pay_till')
    list_filter = ('status', 'pay_till')


admin.site.register(Booking, BookingAdmin)
