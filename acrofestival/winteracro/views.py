from django.shortcuts import render
from .models import (
    Workshop,
    Day,
    Entrie,
)


def fest_homeview(request):
    template_name = 'pages/winteracro/index.html'
    qs_fri = Entrie.objects.filter(when__day="Friday").order_by('time')
    qs_sat = Entrie.objects.filter(when__day="Saturday").order_by('time')
    qs_sun = Entrie.objects.filter(when__day="Sunday").order_by('time')
    qs_mon = Entrie.objects.filter(when__day="Monday").order_by('time')
    qs_tue = Entrie.objects.filter(when__day="Tuesday").order_by('time')
    qs_wed = Entrie.objects.filter(when__day="Wednesday").order_by('time')
    context = {
        "fri": qs_fri,
        "sat": qs_sat,
        "sun": qs_sun,
        "mon": qs_mon,
        "tue": qs_tue,
        "wed": qs_wed,
    }
    return render(request, template_name, context)


def fest_locationview(request):
    template_name = 'pages/winteracro/location.html'
    context = {}
    return render(request, template_name, context)


def fest_pricesview(request):
    template_name = 'pages/winteracro/prices.html'
    context = {}
    return render(request, template_name, context)


def fest_workshopsview(request):
    template_name = 'pages/winteracro/workshops.html'
    qs_jueves = Workshop.objects.filter(date='2018-03-08').order_by('time')
    qs_viernes = Workshop.objects.filter(date='2018-03-09').order_by('time')
    qs_sabado = Workshop.objects.filter(date='2018-03-10').order_by('time')
    qs_domingo = Workshop.objects.filter(date='2018-03-11').order_by('time')
    context = {
        "jueves": qs_jueves,
        "viernes": qs_viernes,
        "sabado": qs_sabado,
        "domingo": qs_domingo
    }
    return render(request, template_name, context)


def frontpage_view(request):
    template_name = 'frontpage.html'
    context = {}
    return render(request, template_name, context)
