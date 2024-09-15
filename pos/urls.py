from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('pos', views.pos, name='pos'),
    path('stock', views.stock, name='stock'),
    path('sales', views.sales, name='sales'),
    path("sales/<int:page>",views.sales,name="sales"),
    path('reports', views.reports, name='reports'),
    path('products', views.products, name='products'),
    path('remove_item/', views.remove_item, name='remove_item'),
    path('receipt/<int:sale_id>', views.receipt, name='receipt'),
    path('save_product', views.save_product, name='save_product'),
    path('receipt/<int:sale_id>', views.receipt, name='sale_receipt'),
    path('add_stock/<str:product_id>', views.add_stock, name='add_stock'),
    path('remove_stock/<str:product_id>', views.remove_stock, name='remove_stock'),
    path('delete_product/<str:product_id>', views.delete_product, name='delete_product'),
    path('update_product/<str:product_id>', views.update_product, name='update_product'),
]
