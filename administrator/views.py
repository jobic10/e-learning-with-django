from django.shortcuts import render

# Administrative Functions


def dashboard(request):
    context = {}
    return render(request, "administrator/home.html", context)
