# from django.shortcuts import render

import logging
from django.http.response import Http404
from django.views.generic import CreateView, ListView

from .forms import ClientCreateForm
from .models import Client


log = logging.getLogger(__name__)


# https://www.agiliq.com/blog/2017/12/when-and-how-use-django-listview/
class ClientList(ListView):
    model = Client
    #clients = Client.objects.exclude(name='public')
    context_object_name = 'clients'
    template_name = "schemas_customers/clients.html"
    paginate_by = 1

    def get_queryset(self):
        clients = Client.objects.exclude(name='public')
        for client in clients:
            client.url = '%s://%s' % (self.request.scheme,
                                      '.'.join([client.name] + self.request.get_host().split('.')[-2:]))
        return clients

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['number'] = context['page_obj'].number
        context['num_pages'] = context['paginator'].num_pages

        '''
        clients = Client.objects.exclude(name='public')
        for client in clients:
            client.url = '%s://%s' % (self.request.scheme,
                                      '.'.join([client.name] + self.request.get_host().split('.')[-2:]))
        context['clients'] = clients
        '''

        return context
    """


# https://www.agiliq.com/blog/2019/01/django-createview/
class ClientCreate(CreateView):
    model = Client
    form_class = ClientCreateForm
    template_name = "schemas_customers/client_create.html"
