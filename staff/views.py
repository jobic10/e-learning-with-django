from django.shortcuts import render, reverse, redirect


# Create your views here.


def path(html_file):
    return f"staff/{html_file}.html"


def dashboard(request):
    context = {}
    return render(request, path("home"), context)
