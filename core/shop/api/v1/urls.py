from django.urls import path, include
from . import views
from django.apps import apps


app_name = "api-v1"

urlpatterns = [
    
    path('<str:store_name>/products/',views.ProductListCreate.as_view(),name="products"),
    path('correct-product-slugs/',views.CorrectProductSlugs.as_view(),name="correct_slugs"),
]