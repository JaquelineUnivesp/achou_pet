# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.http import HttpResponse
from apps.accounts.views import CustomEmailConfirmView

from django.conf.urls.static import static

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/confirm-email/<str:key>/', CustomEmailConfirmView.as_view(), name='account_confirm_email'),
    path('account/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),

    path('api/auth/', include('dj_rest_auth.urls')),
    path('', include('apps.core.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('pet_registration/', include('apps.pet_registration.urls')),
    path('search/', include('apps.search.urls')),
    path('healthz', health_check),

 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


