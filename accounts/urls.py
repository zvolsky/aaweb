from django.contrib.auth import views as auth_views
from django.urls import path

from accounts import views as accounts_views


urlpatterns = [
    path('signup/', accounts_views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
