from django.shortcuts import render
from .forms import BookingForm
from .models import Booking

# Create your views here.
def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            obj = Booking.objects.create(
                name         = form.cleaned_data.get('name'),
                address      = form.cleaned_data.get('address'),
                numero       = form.cleaned_data.get('numero'),
                email        = form.cleaned_data.get('email'),
                option       = form.cleaned_data.get('option'),
                comment      = form.cleaned_data.get('comment')
               )
        if form.errors:
            print(form.errors)
    template_name='pages/home.html'
    context={}
    return render (request, template_name, context)
