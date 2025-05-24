from django.shortcuts import render
from django.views.decorators.cache import never_cache


def home_page(request):
    return render(request, 'home.html')


