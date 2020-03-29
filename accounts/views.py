from django.contrib.auth import login as login
from django.shortcuts import redirect, render

from users.forms import HOME_URL, CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(HOME_URL)
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})
