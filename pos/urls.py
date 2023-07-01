from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('product', views.product, name='product')
]