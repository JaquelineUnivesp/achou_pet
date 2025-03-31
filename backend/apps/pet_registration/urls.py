# backend/apps/pet_registration/urls.py
from django.urls import path
from . import views
from .views import user_pets_list
from .views import pet_detail, edit_pet, delete_pet, user_pets_list
from django.conf.urls.static import static




app_name = 'pet_registration'
urlpatterns = [

# Geral
    path('success/', views.success_view, name='success'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('reverse_geocode/', views.reverse_geocode, name='reverse_geocode'),


    path('register/', views.register_lost_pet, name='register_lost_pet'),
    path('success/', views.success_view, name='success'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('reverse_geocode/', views.reverse_geocode, name='reverse_geocode'),
    path('pets_user/', views.user_pets_list, name='user_pets_list'),
    path('pet/<int:pet_id>/', pet_detail, name='pet_detail'),
    path('pet/<int:pet_id>/editar/', edit_pet, name='edit_pet'),
    path('pet/<int:pet_id>/deletar/', delete_pet, name='delete_pet'),
    path('adoption/register/', views.register_adoption_pet, name='register_adoption_pet'),
    path('breeding/register/', views.register_breeding_pet, name='register_breeding_pet'),  # Nova rota


    path('adoption_pet/<int:pet_id>/', views.adoption_pet_detail, name='adoption_pet_detail'),
    path('breeding_pet/<int:pet_id>/', views.breeding_pet_detail, name='breeding_pet_detail'),
    path('adoption_pet/<int:pet_id>/edit/', views.edit_adoption_pet, name='edit_adoption_pet'),
    path('breeding_pet/<int:pet_id>/edit/', views.edit_breeding_pet, name='edit_breeding_pet'),
    path('adoption_pet/<int:pet_id>/delete/', views.delete_adoption_pet, name='delete_adoption_pet'),
    path('breeding_pet/<int:pet_id>/delete/', views.delete_breeding_pet, name='delete_breeding_pet'),
    path('search/adoption/', views.search_adoption_pets, name='search_adoption_pets'),


]