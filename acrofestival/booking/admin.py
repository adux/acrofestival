from django.contrib import admin
from .models import WinterAcroBooking, UrbanAcroBooking

# Register your models here.


class UrbanAcroBookingAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "name",
        "email",
        "phone",
        "option",
        "comment",
        "status",
        "pay_till")
    list_filter = ("status", "pay_till")


class WinterAcroBookingAdmin(admin.ModelAdmin):
    list_display = (
        "datetime",
        "name",
        "email",
        "phone",
        "address",
        "option",
        "allergies",
        "status",
        "pay_till",
        "pay_date",
        "amount",
        "donation",
    )
    list_filter = ("datetime", "option", "status")
    search_fields = ("name", "email")


admin.site.register(UrbanAcroBooking, UrbanAcroBookingAdmin)
admin.site.register(WinterAcroBooking, WinterAcroBookingAdmin)
