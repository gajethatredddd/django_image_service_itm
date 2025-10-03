from django.urls import path
from . import views

app_name = 'images_api'

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload/', views.image_upload, name='image_upload'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('image/<int:pk>/delete/', views.image_delete, name='image_delete'),
    path('api/image/<int:pk>/delete/', views.image_delete_ajax, name='image_delete_ajax'),
]