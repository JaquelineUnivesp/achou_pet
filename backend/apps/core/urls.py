# backend/apps/core/urls.py
from django.urls import path
from .views import home_view, contato_view, sobre_view, como_funciona_view, faq_view, privacidade_view, termos_view

urlpatterns = [
    path('', home_view, name='home'),
    path('contato/', contato_view, name='contato'),
    path('sobre/', sobre_view, name='sobre'),
    path('como-funciona/', como_funciona_view, name='como_funciona'),
    path('faq/', faq_view, name='faq_funciona'),
    path('privacidade/', privacidade_view, name='privacidade'),
    path('termos/', termos_view, name='termos'),

]