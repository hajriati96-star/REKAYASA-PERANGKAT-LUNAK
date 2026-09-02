from django.urls import path
from . import views

app_name = 'pengembalian'

urlpatterns = [
    path('', views.PengembalianListView.as_view(), name='list'),
    path('tambah/', views.PengembalianCreateView.as_view(), name='tambah'),
    path('<int:pk>/', views.PengembalianDetailView.as_view(), name='detail'),
]
