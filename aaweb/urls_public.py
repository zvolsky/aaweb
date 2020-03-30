from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', admin.site.urls),

    # aaweb/schemas_customers non-i18n urls (? all, that is not needed for search engines ?)
    path('', include('schemas_customers.urls')),
]

urlpatterns.extend(
    i18n_patterns(
        path('', include(('schemas_customers.urls_i18n', 'schemas_customers'), namespace='schemas_customers')),
        path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
        path('users/', include(('users.urls', 'users'), namespace='users')),
    )
)


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
