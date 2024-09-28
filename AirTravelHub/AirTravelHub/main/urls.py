from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='main/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('flight_search/', views.flight_search, name='flight_search'),
    path('account/', views.account, name='account'),
    path('autocomplete/country/', views.country_autocomplete, name='country_autocomplete'),
]