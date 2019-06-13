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
                name=form.cleaned_data.get('name'),
                address=form.cleaned_data.get('address'),
                numero=form.cleaned_data.get('numero'),
                email=form.cleaned_data.get('email'),
                option=form.cleaned_data.get('option'),
                comment=form.cleaned_data.get('comment')
               )
        if form.errors:
            print(form.errors)
    template_name = 'pages/urbanacro/home.html'
    context = {}
    return render(request, template_name, context)


def winteracroform_view(request):
    if request.method == "POST":
        form = WinterAcroForm(request.POST)
        if form.is_valid():
            obj = WinterAcroBooking.objects.create(
                name=form.cleaned_data.get('name'),
                address=form.cleaned_data.get('address'),
                numero=form.cleaned_data.get('numero'),
                email=form.cleaned_data.get('email'),
                option=form.cleaned_data.get('option'),
                allergies=form.cleaned_data.get('allergies')
                )
            subject = 'Winter Acro Festival 2019'
            message = "Hoi " + obj.name + "\r\n\r\nThanks for registering for the Winter Acro Festival 2019!\r\n\r\nLamas are little rebels, they are not good at doing automatic jobs. Definitly not as good as monkeys. Fly better though...\r\n\r\nAnyway, in the next 72 hours you will receive an email concerning your registration status. So just like Axl Rose said: Gotta have some patience.\r\n\r\n\r\nBig Hug\r\nThe Lamas"
            sender = 'notmonkeys@acrofestival.ch'
            to = [obj.email]
            send_mail(subject, message, sender, to)
        if form.errors:
            print(form.errors)
    template_name = 'pages/formulario/homeform.html'
    context = {}
    return render(request, template_name, context)
