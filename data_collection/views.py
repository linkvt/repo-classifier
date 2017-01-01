from random import randint

import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from classification.GithubAuthentification import GithubAuthentification
from classification.models import Repository

GITHUB_PREFIX = 'https://github.com'


def index(request):
    return HttpResponse("Hello at the data collection index")


def random_repo(request: HttpRequest) -> HttpResponse:
    url = request.POST.get('url')
    selected_category = request.POST.get('category')

    if url and selected_category:
        Repository.objects.create(url=url, category=selected_category)

    github = GithubAuthentification()
    # 77000000 is roughly the number of public repos
    since = randint(1, 77000000)
    repo = github.get_repos(since).get_page(1)[0]

    context = {
        'url': repo.html_url,
        'name': repo.name,
        'owner': repo.owner.login,
        'owner_url': repo.owner.html_url,
        'description': repo.description,
        'categories': Repository.CATEGORIES
    }
    return render(request, 'data_collection/random_repo.html', context)


def showcase_urls(request: HttpRequest) -> HttpResponse:
    showcase_url = request.POST.get('showcase_url')

    if showcase_url:
        webpage = requests.get(showcase_url).text
        soup = BeautifulSoup(webpage)
        tags = soup.select('h3.mb-1 a')
        urls = [GITHUB_PREFIX + tag['href'] for tag in tags]
    else:
        urls = []

    context = {
        'urls': urls,
        'selected_category': request.POST.get('category'),
        'categories': Repository.CATEGORIES,
    }
    return render(request, 'data_collection/showcase_urls.html', context)
