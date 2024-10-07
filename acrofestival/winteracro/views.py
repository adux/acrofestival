from django.shortcuts import render
from .models import Workshop, Day, Entrie


def fest_homeview(request):
    template_name = "pages/winteracro/index.html"
    qs = Entrie.objects.all().order_by('time').select_related('when')
    qs_sat1 = qs.filter(when__day="Saturday1")
    qs_sat2 = qs.filter(when__day="Saturday2")
    qs_sun = qs.filter(when__day="Sunday")
    qs_mon = qs.filter(when__day="Monday")
    qs_tue = qs.filter(when__day="Tuesday")
    qs_wed = qs.filter(when__day="Wednesday")
    qs_thu = qs.filter(when__day="Thursday")
    qs_fri = qs.filter(when__day="Friday")
    context = {
        "sat1": qs_sat1,
        "sat2": qs_sat2,
        "sun": qs_sun,
        "mon": qs_mon,
        "tue": qs_tue,
        "wed": qs_wed,
        "thu": qs_thu,
        "fri": qs_fri,
    }
    return render(request, template_name, context)


def fest_locationview(request):
    template_name = "pages/winteracro/location.html"
    context = {}
    return render(request, template_name, context)

def fest_accommodationview(request):
    template_name = "pages/winteracro/accommodation.html"
    context = {}
    return render(request, template_name, context)


def fest_conditionsview(request):
    template_name = "pages/winteracro/conditions.html"
    context = {}
    return render(request, template_name, context)


def fest_picturesview(request):
    template_name = "pages/winteracro/pictures.html"
    context = {}
    return render(request, template_name, context)


def fest_workshopsview(request):
    template_name = "pages/winteracro/workshops.html"
    qs_jueves = Workshop.objects.filter(date="2018-03-08").order_by("time")
    qs_viernes = Workshop.objects.filter(date="2018-03-09").order_by("time")
    qs_sabado = Workshop.objects.filter(date="2018-03-10").order_by("time")
    qs_domingo = Workshop.objects.filter(date="2018-03-11").order_by("time")
    context = {
        "jueves": qs_jueves,
        "viernes": qs_viernes,
        "sabado": qs_sabado,
        "domingo": qs_domingo,
    }
    return render(request, template_name, context)


def frontpage_view(request):
    template_name = "frontpage.html"
    context = {}
    return render(request, template_name, context)
