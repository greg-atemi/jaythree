from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('stock', views.stock, name='stock'),
    path('', views.dashboard, name='dashboard'),
    path('products', views.products, name='products'),
    path('add_stock/<str:product_id>', views.add_stock, name='add_stock'),
    path('save_product/<str:product_id>', views.save_product, name='save_product'),
    path('remove_stock/<str:product_id>', views.remove_stock, name='remove_stock'),
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('update_product/<str:product_id>', views.update_product, name='update_product'),
]
