from django import views
from pos import views
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pos/', include('pos.urls')),
    path('', views.dashboard, name='dashboard'),
    path('accounts/login/', views.login, name='login')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
