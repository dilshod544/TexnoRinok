from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .admin_site import custom_admin_site
from django.shortcuts import redirect
from django.views.generic import TemplateView, RedirectView

from django.contrib.sitemaps.views import sitemap
from apps.products.sitemaps import ProductSitemap, CategorySitemap, StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
}

from django.http import HttpResponse

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('health/', lambda r: HttpResponse("OK")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/favicon.png?v=2')),
    path('admin/', lambda r: redirect('store_admin:dashboard')),
    path('django-admin/', custom_admin_site.urls),
    path('admin-panel/', include('apps.store_admin.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('accounts/', include('apps.accounts.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


