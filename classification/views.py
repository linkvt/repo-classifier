from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from classification import classifier
from classification.evaluation.LanguageAnalyser import LanguageAnalyser
from classification.evaluation.DescriptionAnalyser import DescriptionAnalyser
from classification.evaluation.FileNameAnalyser import FileNameAnalyser
from classification.models import Feature


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


def analysis(request: HttpRequest) -> HttpResponse:
    uploaded_file = request.FILES.get('file')
    subject = request.POST.get('subject')

    result = ''
    if uploaded_file:
        data = uploaded_file.read()
        text = data.decode(uploaded_file.charset or 'utf-8')

        analyser = None
        if subject == 'description':
            analyser = DescriptionAnalyser()
        elif subject == 'filename':
            analyser = FileNameAnalyser()
        elif subject == 'language':
            analyser = LanguageAnalyser()
        analyser.text = text
        result = analyser.analyse(text)

    context = {
        'output': result,
    }

    return render(request, 'classification/analysis.html', context)


def dbactions(request: HttpRequest) -> HttpResponse:
    remove_group_button = request.POST.get('remove_group')
    group_to_remove = request.POST.get('group_to_remove')
    available_names = [item["name"] for item in Feature.objects.values('name').distinct()]
    result = ''

    if remove_group_button and group_to_remove:
        result = '%i features have been deleted.' % Feature.objects.filter(name=group_to_remove).delete()[0]

    context = {
        'output': result,
        'name_fields': available_names
    }

    return render(request, 'classification/dbactions.html', context)
