# from django.shortcuts import render

import logging
from django.http.response import Http404
from django.views.generic import ListView, DetailView, TemplateView


log = logging.getLogger(__name__)


class IndexView(TemplateView):
    template_name = "schemas_customers/index.html"

    def get_context_data(self, **kwargs):
        # TODO: what we offer...
        return super().get_context_data(**kwargs)
