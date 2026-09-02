from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('daftar/', views.RegistrasiView.as_view(), name='registrasi'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
]
