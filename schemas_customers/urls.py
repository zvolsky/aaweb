from django.urls import path

from schemas_customers import views

urlpatterns = [
    path('', views.TenantList.as_view(), name='home'),
    path('create/', views.TenantCreate.as_view(), name='create'),
]
