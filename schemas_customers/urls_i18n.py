from django.urls import include, path

from schemas_customers import views

urlpatterns = [
    path('', views.ClientList.as_view(), name='home'),
    path('create/', views.ClientCreate.as_view(), name='create'),
]
