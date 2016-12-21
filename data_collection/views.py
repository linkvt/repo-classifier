import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import loader

from classification.models import Repository

GITHUB_PREFIX = 'https://github.com'


def index(request):
    return HttpResponse("Hello at the data collection index")


def showcase_urls(request: HttpRequest) -> HttpResponse:
    showcase_url = request.POST.get('showcase_url')
    urls = []

    if showcase_url:
        webpage = requests.get(showcase_url).text
        soup = BeautifulSoup(webpage)
        tags = soup.select('h3.mb-1 a')
        urls = [GITHUB_PREFIX + tag['href'] for tag in tags]

    template = loader.get_template('data_collection/showcase_urls.html')
    context = {
        'urls': urls,
        'selected_category': request.POST.get('category'),
        'categories': Repository.CATEGORIES,
    }
    return HttpResponse(template.render(context, request))
