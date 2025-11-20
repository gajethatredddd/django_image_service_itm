from django.urls import path, include
from rest_framework import routers
from . import views
from .views import NewViewSet
from rest_framework_simplejwt.views import (TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'images_api'
router = routers.DefaultRouter()
router.register(r'lol', NewViewSet)

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('api/v1/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/available-ids/', views.available_ids, name='available-ids'),

    path('upload/', views.image_upload, name='image_upload'),
    path('image/<int:pk>/', views.image_detail, name='image_detail'),
    path('image/<int:pk>/delete/', views.image_delete, name='image_delete'),
    path('api/image/<int:pk>/delete/', views.image_delete_ajax, name='image_delete_ajax'),
]

