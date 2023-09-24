from django.urls import path
from .views import home_view, product_details, accessed_products, lesson_details
from .api import LessonsListAPIView, ProductLessonsListAPIView, ProductStatisticsAPIView

app_name = "products"


urlpatterns = [
    path("", home_view, name="home"),
    path("product/<int:pk>", product_details, name='product-details'),
    path("accessed-products", accessed_products, name='accessed-products'),
    path("lesson/<int:product_id>/<int:lesson_id>", lesson_details, name='lesson-details'),
    path("api/v1/all-lessons", LessonsListAPIView.as_view(), name='accessed-lessons-list'),
    path('api/v1/statistics', ProductStatisticsAPIView.as_view(), name='statistics'),
    path("api/v1/product-lessons/<int:product_id>", ProductLessonsListAPIView.as_view(), name='product-lessons-list'),
]
