from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('programs/', views.specialty_list_view, name='specialty_list'),
    path('programs/<int:pk>/', views.specialty_detail_view, name='specialty_detail'),
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/<int:pk>/', views.department_detail_view, name='department_detail'),
    path('contacts/', views.contacts_view, name='contacts'),
]
