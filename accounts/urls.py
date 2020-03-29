from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.conf.urls import url

from accounts import views as accounts_views


urlpatterns = [
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/pwd/reset.html',
            email_template_name='accounts/pwd/reset_email.html',
            subject_template_name='accounts/pwd/reset_subject.txt',
            success_url = reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/pwd/reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/pwd/reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/pwd/reset_complete.html'),
        name='password_reset_complete'),
]
