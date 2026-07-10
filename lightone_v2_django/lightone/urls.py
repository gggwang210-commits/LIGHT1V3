from django.urls import path
from . import views

app_name = 'lightone'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('method/', views.method, name='method'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('session/new/', views.session_create, name='session_create'),
]
