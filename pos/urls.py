from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('pos', views.pos, name='pos'),
    path('stock', views.stock, name='stock'),
    path('products', views.products, name='products'),
    path('sales', views.sales, name='sales'),
    path('reports', views.reports, name='reports'),
    path('receipt/<int:sale_id>', views.receipt, name='receipt'),
    path('receipt/<int:sale_id>', views.receipt, name='sale_receipt'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('save_product', views.save_product, name='save_product'),
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('update_product/<str:product_id>', views.update_product, name='update_product'),
    path('add_stock/<str:product_id>', views.add_stock, name='add_stock'),
    path('remove_stock/<str:product_id>', views.remove_stock, name='remove_stock'),
]
