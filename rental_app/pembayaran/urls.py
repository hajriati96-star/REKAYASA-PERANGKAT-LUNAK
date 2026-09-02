from django.urls import path
from . import views

app_name = 'pembayaran'

urlpatterns = [
    path('', views.PembayaranListView.as_view(), name='list'),
    path('tambah/', views.PembayaranCreateView.as_view(), name='tambah'),
    path('<int:pk>/', views.PembayaranDetailView.as_view(), name='detail'),
]
