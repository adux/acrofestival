from django.shortcuts import render
from django.core.mail import send_mail
from .forms import UrbanAcroForm, WinterAcroForm
from .models import UrbanAcroBooking, WinterAcroBooking


# Create your views here.
def urbanacro_view(request):
    if request.method == "POST":
        form = UrbanAcroForm(request.POST)
        if form.is_valid():
            obj = UrbanAcroBooking.objects.create(
                name=form.cleaned_data.get("name"),
                address=form.cleaned_data.get("address"),
                phone=form.cleaned_data.get("numero"),
                email=form.cleaned_data.get("email"),
                option=form.cleaned_data.get("option"),
                comment=form.cleaned_data.get("comment"),
            )
            subject = "Urban Acro Festival 2020"
            message = (
                "Hoi "
                + obj.name
                + "\r\n\r\nThanks for registering for the Urban Acro Festival 2020!\r\n\r\nLamas are little rebels, they are not good at doing automatic jobs. Definitly not as good as monkeys. Fly better though...\r\n\r\nAnyway, we'll get to you as soon as possible concerning your registration status. So just like Axl Rose said: Gotta have some patience.\r\n\r\n\r\nBig Hug\r\nThe Lamas"
            )
            sender = "notmonkeys@acrofestival.ch"
            to = [obj.email]
            send_mail(subject, message, sender, to)
        if form.errors:
            print(form.errors)
    template_name = "pages/urbanacro/home.html"
    context = {}
    return render(request, template_name, context)


def winteracroform_view(request):
    if request.method == "POST":
        form = WinterAcroForm(request.POST)
        if form.is_valid():
            obj = WinterAcroBooking.objects.create(
                name=form.cleaned_data.get("name"),
                address=form.cleaned_data.get("address"),
                phone=form.cleaned_data.get("phone"),
                email=form.cleaned_data.get("email"),
                option=form.cleaned_data.get("option"),
                allergies=form.cleaned_data.get("allergies"),
                donation=form.cleaned_data.get("donation"),
            )
            subject = "Winter Acro Festival 2020"
            message = (
                "Hoi "
                + obj.name
                + "\r\n\r\nThanks for registering for the Winter Acro Festival 2020!\r\n\r\nAn entire operation has begun. A herd of lamas is inspecting carefully your registration. No worries, you're in good hands.\r\n\r\nWe'll get back to you as soon as possible. If you are nervous about the results and can't sleep: count lamas, it helps.\r\n\r\n\r\nBig Hug\r\nThe Lamas"
            )
            sender = "noreply@acrofestival.ch"
            to = [obj.email]
            send_mail(subject, message, sender, to)
        if form.errors:
            print(form.errors)
    template_name = "pages/formulario/homeform.html"
    context = {}
    return render(request, template_name, context)
