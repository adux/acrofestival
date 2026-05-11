from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views import defaults as default_views
from django.views.generic import TemplateView
from booking.views import (urbanacro_view, winteracroform_view)
from winteracro.views import (
    fest_homeview,
    fest_locationview,
    fest_accommodationview,
    fest_conditionsview,
    fest_picturesview,
    frontpage_view,
    )
from dap.views import dap_view
from acrofestival.sitemaps import StaticViewSitemap


sitemaps = {"static": StaticViewSitemap}

urlpatterns = [
    path("", frontpage_view, name="home"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path(settings.ADMIN_URL, admin.site.urls),
    path("content-editor/", include("acrofestival.content.urls", namespace="content")),
    path("dap/", dap_view, name="dap"),
    path("urbanacro/", urbanacro_view, name="urbanacro"),
    path("winteracro/", fest_homeview, name="winteracro"),
    path("pictures/", fest_picturesview, name="pictures"),
    path("winteracro/form/", winteracroform_view, name="winterform"),
    path("winteracro/location", fest_locationview, name="winterlocation"),
    path("winteracro/accommodation", fest_accommodationview, name="winteraccommodation"),
    path("winteracro/conditions", fest_conditionsview, name="winterconditions"),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
