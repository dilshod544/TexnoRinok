from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('address/new/', views.address_create, name='address_create'),
    path('address/<int:pk>/edit/', views.address_update, name='address_update'),
    path('address/<int:pk>/delete/', views.address_delete, name='address_delete'),
]
