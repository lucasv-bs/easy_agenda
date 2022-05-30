# django imports
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# project imports
from . import views

app_name = "consultation"

urlpatterns = [
    path('<int:id>/', views.consultation, name='consultation'),
    path('<int:id>/save/', views.save, name='save-consultation')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)