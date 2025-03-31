# backend/apps/core/views.py
from django.shortcuts import render
from . import views

def home_view(request):
    return render(request, 'core/home.html')

def contato_view(request):
    return render(request, 'core/contato.html')

def sobre_view(request):
    return render(request, 'core/sobre.html')

def como_funciona_view(request):
    return render(request, 'core/como_funciona.html')

def faq_view(request):
    return render(request, 'core/faq.html')

def privacidade_view(request):
    return render(request, 'core/privacidade.html')

def termos_view(request):
    return render(request, 'core/termos.html')

