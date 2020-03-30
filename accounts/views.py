from django.conf import settings
from django.contrib.auth import login, views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from users.forms import CustomUserCreationForm


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = settings.HOME_URL
        return context


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['home_url'] = settings.HOME_URL
        return context


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
