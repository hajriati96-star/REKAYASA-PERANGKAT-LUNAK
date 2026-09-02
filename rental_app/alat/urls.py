from django.urls import path
from . import views

app_name = 'alat'

urlpatterns = [
    path('', views.AlatListView.as_view(), name='list'),
    path('tambah/', views.AlatCreateView.as_view(), name='tambah'),
    path('<int:pk>/', views.AlatDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.AlatUpdateView.as_view(), name='edit'),
    path('<int:pk>/hapus/', views.AlatDeleteView.as_view(), name='hapus'),
]
