from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.product_list, name='list'),
    path('product/<slug:slug>/', views.product_detail, name='detail'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('delivery/', views.delivery_view, name='delivery'),
    path('contact/', views.contact_view, name='contact'),
]
