from django.contrib.auth.forms import UserCreationForm

# Django 3.0.4-(+?) bug, User hardcoded in forms.py instead of get_user_model()
from django.contrib.auth.forms import UserModel, UsernameField  # forms.py assigns: UserModel = get_user_model()


HOME_URL = 'schemas_customers:home'


class CustomUserCreationForm(UserCreationForm):
    Meta = UserCreationForm
    Meta.model = UserModel  # workaround for Django 3.0.4-(+?) bug, User hardcoded in forms.py instead of get_user_model()
    Meta.fields = ('username', 'email', 'password1', 'password2')
    Meta.field_classes = {'username': UsernameField}
