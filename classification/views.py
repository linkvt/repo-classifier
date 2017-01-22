from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from github import RateLimitExceededException

from classification import classifier
from classification.evaluation.DescriptionAnalyser import DescriptionAnalyser
from classification.evaluation.FileExtensionAnalyser import FileExtensionAnalyser
from classification.evaluation.FileNameAnalyser import FileNameAnalyser
from classification.evaluation.LanguageAnalyser import LanguageAnalyser
from classification.models import Feature


def index(request: HttpRequest) -> HttpResponse:
    uploaded_file = request.FILES.get('file')
    url = request.POST['repo-url'] if 'repo-url' in request.POST else None
    mode = request.POST['mode'] if 'mode' in request.POST else None
    if mode and uploaded_file:
        data = uploaded_file.read()
        text = data.decode(uploaded_file.charset or 'utf-8')
    else:
        text = None

    output_lines = ''
    reports = None
    validation_output = None

    try:
        if mode == 'train':
            output_lines, reports = classifier.train(text) if text else ([], None)
        elif mode == 'classify':
            output_lines = classifier.classify(text) if text else None
        elif mode == 'classify-single-repo':
            output_lines = classifier.classify_single_repo(url.rstrip('/')) if url else None
        elif mode == 'validate':
            validation_output = classifier.validate(text) if text else None
    except RateLimitExceededException:
        output_lines = 'The available request limit was exceeded for the Github API please wait until refresh.'

    context = {
        'output': output_lines,
        'validation_output': validation_output,
        'single_repository': url,
        'reports': reports,
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
        elif subject == 'extension':
            analyser = FileExtensionAnalyser()
        analyser.text = text
        result = analyser.analyse(text)

    context = {
        'output': result,
    }

    return render(request, 'classification/analysis.html', context)


def dbactions(request: HttpRequest) -> HttpResponse:
    mode = request.POST.get('mode')
    group_to_remove = request.POST.get('group_to_remove')
    deleted_features = None

    if mode == 'name_group_removal' and group_to_remove:
        deleted_features = Feature.objects.filter(name=group_to_remove).delete()[0]
    elif mode == 'all':
        deleted_features = Feature.objects.all().delete()[0]

    result = '%i features have been deleted.' % deleted_features if deleted_features is not None else ''
    available_names = [item["name"] for item in Feature.objects.values('name').distinct()]
    context = {
        'output': result,
        'name_fields': available_names
    }

    return render(request, 'classification/dbactions.html', context)


def vis(request: HttpRequest) -> HttpResponse:
    return render(request, 'classification/vis.html')


def histogram(request):
    return render(request, 'classification/histogram.html')
