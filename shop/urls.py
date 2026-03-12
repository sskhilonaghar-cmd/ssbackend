from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'gallery', views.GalleryImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.admin_login, name='admin-login'),
]
