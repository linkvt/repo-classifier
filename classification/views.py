from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from classification import classifier


def index(request: HttpRequest) -> HttpResponse:
    uploaded_file = request.FILES.get('file')
    mode = request.POST['mode'] if 'mode' in request.POST else None
    if mode and uploaded_file:
        data = uploaded_file.read()
        text = data.decode(uploaded_file.charset or 'utf-8')
    else:
        text = None

    output_lines = ''
    if mode == 'train':
        output_lines = list(classifier.train(text)) if text else []
    elif mode == 'classify':
        output_lines = list(classifier.classify(text)) if text else []

    context = {
        'output': '\n'.join(output_lines),
    }

    return render(request, 'classification/index.html', context)
