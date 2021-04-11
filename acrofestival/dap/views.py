from django.shortcuts import render

# Create your views here.


def dap_view(request):
    template_name = "pages/dap/index.html"
    context = {}

    return render(request, template_name, context)
