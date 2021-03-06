import requests
import time

from django.http import HttpResponse


def stackoverflow(get_response):
    def middleware(request):
        # This method does nothing, all we want is exception processing
        return get_response(request)

    def process_exception(request, exception):
        url = 'https://api.stackexchange.com/2.2/search'
        params = {
            'site': 'stackoverflow',
            'order': 'desc',
            'sort': 'votes',
            'pagesize': 3,
            'tagged': 'python;django',
            'intitle': str(exception),
        }
        response = requests.get(url, params=params)
        html = ''
        for question in response.json()['items']:
            html += '<h2><a href="{link}">{title}</a></h2>'.format(**question)
        return HttpResponse(html)

    middleware.process_exception = process_exception

    return middleware

class StackOverflow:
   def __init__(self, get_response):
       self.get_response = get_response

   def __call__(self, request):
       return self.get_response(request)

   def process_exception(request, exception):
        print(50 * '-')
        print(exception.__class__.__name__)
        print(exception.message)
        print(50 * '-')
        return None
        '''
        import pdb; pdb.set_trace()
        url = 'https://api.stackexchange.com/2.2/search'
        params = {
            'site': 'stackoverflow',
            'order': 'desc',
            'sort': 'votes',
            'pagesize': 3,
            'tagged': 'python;django',
            'intitle': str(exception),
        }
        response = requests.get(url, params=params)
        html = ''
        for question in response.json()['items']:
            html += '<h2><a href="{link}">{title}</a></h2>'.format(**question)
        return HttpResponse(html)
        '''


def timing(get_response):
    def middleware(request):
        print(getattr(request, 'user', '-------'))  # debug tool, after AuthenticationMiddleware
        t1 = time.time()
        response = get_response(request)
        t2 = time.time()
        print(f"{request.path} :TOTAL TIME: {t2 - t1}")
        return response
    return middleware
