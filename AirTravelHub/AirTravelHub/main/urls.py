from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='main/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('flights/', views.flights, name='flights'),
    path('document/', views.document, name='document'),
    path('document_redact', views.document_redact, name='document_redact'),
    path('autocomplete/country/', views.country_autocomplete, name='country_autocomplete'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('passenger_info', views.passenger_info, name='passenger_info'),
    path('seat', views.seat, name='seat'),
    path('payment/', views.payment, name='payment'),
    path('api/passenger_data/', views.passenger_data, name='passenger_data'),
    path('success/', views.success, name='success'),
    path('card/', views.card, name='card')
]