from django.urls import path
from .views import home_view, product_details, accessed_products, lesson_details

app_name = "products"


urlpatterns = [
    path("", home_view, name="home"),
    path("product/<int:pk>", product_details, name='product-details'),
    path("accessed-products", accessed_products, name='accessed-products'),
    path("lesson/<int:product_id>/<int:lesson_id>", lesson_details, name='lesson-details'),
]
