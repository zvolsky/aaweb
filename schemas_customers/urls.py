from django.urls import path

from schemas_customers import views

urlpatterns = [
    path('', views.TenantList.as_view(), name='home'),
    path('create/', views.TenantCreate.as_view(), name='create'),
    path('creating/', views.TenantCreating.as_view(), name='creating'),

    path('ajax/is_site_ready/', views.is_site_ready, name='is_site_ready'),
]
