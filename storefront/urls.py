from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.urls import include, path, re_path
from debug_toolbar.toolbar import debug_toolbar_urls

admin.site.site_header = "StoreFront Admin"
admin.site.index_title = "Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("playground/", include("playground.urls")),
    path("store/", include("store.urls")),
    re_path(r"^auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.jwt")),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
