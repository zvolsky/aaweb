from django.contrib.auth.models import AbstractUser
from django.db import models


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser
class User(AbstractUser):
    gdpr = models.DateTimeField(null=True, blank=True)

    '''
    @staticmethod
    def autocomplete_search_fields():
        return 'username', 'last_name'

    def __str__(self):
        fullname = '{} {}'.format(self.first_name, self.last_name)

        if fullname == ' ':
            return self.username
        return '{} - {}'.format(self.username, fullname)
    '''
