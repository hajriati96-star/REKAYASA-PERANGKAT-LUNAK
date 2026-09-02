from django.urls import path
from . import views

app_name = 'penyewaan'

urlpatterns = [
    path('', views.PenyewaanListView.as_view(), name='list'),
    path('tambah/', views.PenyewaanCreateView.as_view(), name='tambah'),
    path('<int:pk>/', views.PenyewaanDetailView.as_view(), name='detail'),
]
