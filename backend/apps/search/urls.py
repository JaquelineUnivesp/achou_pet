from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'search'

urlpatterns = [
    path('', views.search_pets, name='search_pets'),
    path('lost/', views.search_lost_pets, name='lost_pets'),
    path('adoption/', views.search_adoption_pets, name='adoption_pets'),
    path('breeding/', views.search_breeding_pets, name='breeding_pets'),
    path('api/pets/', views.api_pets, name='api_pets'),
    path('api/user-location/', views.get_user_location, name='get_user_location'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)