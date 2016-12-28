from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from classification import classifier

SAMPLE_FILE = 'repositories_sample.csv'


def index(request: HttpRequest) -> HttpResponse:
    uploaded_file = request.FILES.get('file')
    if uploaded_file:
        data = uploaded_file.read()
        text = data.decode(uploaded_file.charset or 'utf-8')
    elif request.POST:
        with open(SAMPLE_FILE) as file:
            text = file.read()
    else:
        text = None

    output_lines = list(classifier.train_and_classify(text)) if text else []

    context = {
        'output': '\n'.join(output_lines),
    }

    return render(request, 'classification/index.html', context)
