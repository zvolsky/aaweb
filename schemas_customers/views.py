import base64
import logging
import os
import shlex
from subprocess import Popen

from tenant_schemas.utils import schema_context

from django.contrib import messages
from django.contrib.auth import get_user_model
#User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http.response import Http404
from django.shortcuts import redirect  # , render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
#from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView

from .forms import TenantCreateForm
from .models import Tenant


log = logging.getLogger(__name__)


# https://www.agiliq.com/blog/2017/12/when-and-how-use-django-listview/
class TenantList(ListView):
    model = Tenant
    #tenants = Tenant.objects.exclude(name='public').exclude(name='extensions')
    context_object_name = 'clients'
    template_name = "schemas_customers/clients.html"
    paginate_by = 10

    def get_queryset(self):
        clients = Tenant.objects.exclude(name='public').filter(publicly=True)
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
        clients = Tenant.objects.exclude(name='public')
        for client in clients:
            client.url = '%s://%s' % (self.request.scheme,
                                      '.'.join([client.name] + self.request.get_host().split('.')[-2:]))
        context['clients'] = clients
        '''

        return context
    """


# https://www.agiliq.com/blog/2019/01/django-createview/ (with lot of mistakes)
@method_decorator(login_required, name='dispatch')
class TenantCreate(CreateView):
    model = Tenant
    form_class = TenantCreateForm
    template_name = "schemas_customers/tenant_create.html"

    def form_valid(self, form):
        user = self.request.user.id
        subdomain = form.cleaned_data['name']
        domain = '.'.join(self.request.get_host().split(':', 1)[0].split('.', 2)[-2:])
        port = self.request.get_port()
        if port in ('80', '443'):
            port = ''
        else:
            port = f':{port}'
        self.request.session['expected_web'] = expected_web = f"{subdomain}.{domain}{port}"
        self.request.session['a_tag'] = f'<a href="{self.request.scheme}://{expected_web}/admin">'

        # run in same virtual environment: https://gist.github.com/turicas/2897697
        ve = '/home/www-data/.virtualenvs/aaweb'
        command_template = f'/bin/bash -c "source {ve}/bin/activate && python --version"'
        command = shlex.split(command_template)
        # replace(' ', ''): in special cases could base64 encoded string contain spaces for readability
        # (not sure if so while base64 is used)
        with open('/home/www-data/dj/aaweb/aaweb/log/out', 'w') as fout:
            with open('/home/www-data/dj/aaweb/aaweb/log/err', 'w') as ferr:
                Popen(command,
                        stdout=fout,
                        stderr=ferr
                        )
        #Popen(('python', 'manage.py',
        #        'create_tenant', '-s', subdomain, '-d', domain, '-u', str(user),
        #        '-b', base64.b64encode(form.cleaned_data['description'].encode()).replace(b' ', b'').replace(b'\n', b'')))

        return redirect(form.success_url)
        # we must finish request first; following or subprocess.run() doesn't work from not exactly known reason
        '''
        self.client = form.save(commit=False)
        self.client.schema_name = self.client.name
        self.client.domain_url = f"{self.client.name}.{'.'.join(self.request.get_host().rsplit('.', 2)[-2:])}"
        self.client.user = self.request.user
        self.client.save()
        '''

@method_decorator(login_required, name='dispatch')
class TenantCreating(TemplateView):
    #extra_context = {...}
    template_name = "schemas_customers/tenant_creating.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['expected_web'] = self.request.session.get('expected_web')
        context['a_tag'] = self.request.session.get('a_tag')
        return context

# ------- ajax -------

#@csrf_exempt
def is_site_ready(request):  # js: Tenant_Creating.isSiteReady
    user = request.user  # radši se toho ani nedotýkám a nepřesouvám dolů, viz níže: problémy
    ready = False
    web = request.GET.get('web')
    if web:
        name = web.split('.', 1)[0]
        try:
            tenant = Tenant.objects.get(name=name)
        except Tenant.DoesNotExist:
            tenant = None
        if tenant and tenant.created_on:
            #with schema_context('public'):                      # při ladění divné problémy: AnonymousUser
            #    user = get_user_model().objects.get(pk=userId)  # pokud znova, přenést userId ajaxem
            with schema_context(tenant.name):
                if not get_user_model().objects.exists():
                    tenant_user = get_user_model().objects.create_superuser(user.username, user.email, 'tmppwd')
                    tenant_user.password = user.password
                    tenant_user.save()
            ready = True
    data = {
        'ready': 'ready' if ready else ''  // True if ready else False
    }
    return JsonResponse(data)
