from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from classification import classifier

REPOSITORIES_SAMPLE_FILE = 'repositories_sample.csv'


def index(request: HttpRequest) -> HttpResponse:
    output_lines = []
    if 'train' in request.POST:
        output_lines = list(classifier.train_and_classify(REPOSITORIES_SAMPLE_FILE))

    context = {
        'output': '\n'.join(output_lines)
    }

    return render(request, 'classification/index.html', context)
