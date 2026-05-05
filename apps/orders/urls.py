from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:pk>/', views.order_success, name='success'),
    path('my-orders/', views.order_list, name='list'),
    path('my-orders/<int:pk>/', views.order_detail, name='detail'),
]
