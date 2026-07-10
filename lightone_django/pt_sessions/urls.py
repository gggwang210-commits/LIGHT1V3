from django.urls import path
from . import views

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('new/', views.session_create, name='session_create'),
    path('<int:pk>/', views.session_detail, name='session_detail'),
]
