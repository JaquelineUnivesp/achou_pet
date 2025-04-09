# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings


from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('apps.accounts.urls')),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('', include('apps.core.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('pet_registration/', include('apps.pet_registration.urls')),
    path('search/', include('apps.search.urls')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)