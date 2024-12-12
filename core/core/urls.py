from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import StoreSitemap, ProductSitemap, CategorySitemap, BlogPostSitemap, ProductImageSitemap, CategoryImageSitemap
from django.views.generic import TemplateView

sitemaps = {
    'stores': StoreSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'blog posts': BlogPostSitemap,
    'product images': ProductImageSitemap,
    'category images': CategoryImageSitemap,
}

from . import views

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", include("shop.urls")),
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    # path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
