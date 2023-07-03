from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products', views.products, name='products'),
    path('save_product', views.save_product, name='save_product'),
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('update_product/<str:product_id>', views.update_product, name='update_product'),
]
