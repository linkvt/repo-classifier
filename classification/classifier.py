import logging

from sklearn.model_selection import train_test_split

from classification.InputParser import InputParser
from classification.algorithm.algorithms import Classifier, RandomForestClassifier, KNeighborsClassifier, MLPClassifier, \
    ExtraTreesClassifier, SVMClassifier
from classification.evaluation.Evaluator import Evaluator
from classification.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline
from classification.models import Repository

logger = logging.getLogger(__name__)
extraction_pipeline = FeatureExtractionPipeline()


def train(text, train=True):
    input_parser = InputParser(text, train)
    splitted_urls, labels = input_parser.parse()
    repositories = map_urls_to_repositories(splitted_urls)

    classifiers = [MLPClassifier(), ExtraTreesClassifier(), RandomForestClassifier(), SVMClassifier(),
                   KNeighborsClassifier()]

    result = ''
    reports = []
    if train:
        samples = extraction_pipeline.extract_features(repositories)

        training_percentage = 0.6
        logger.info(
            'Splitting into {:.0%} training and {:.0%} test data.'.format(training_percentage, 1 - training_percentage))
        train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels,
                                                                                  test_size=1 - training_percentage,
                                                                                  random_state=0, stratify=labels)
        for clf in classifiers:
            clf.fit(train_samples, train_labels)
            predict_labels = clf.predict(test_samples)

            evaluator = Evaluator(clf, test_labels, predict_labels)
            result += evaluator.report() + '\n'
            reports.append((clf.name, evaluator.confusion_matrix_raw(), evaluator.report_raw()))

        classifiers[0].save()
    return result, reports


def classify(text):
    input_parser = InputParser(text, train=False)
    urls, _ = input_parser.parse()
    repos = map_urls_to_repositories(urls)

    clf = Classifier.load()

    if not clf:
        return 'No trained model available.'

    samples = extraction_pipeline.extract_features(repos)

    labels = clf.predict(samples)

    result = '\n'.join(url + ' ' + label for url, label in list(zip(urls, labels)))

    return result


def validate(text):
    response = Response()
    input_parser = InputParser(text, True)
    splitted_urls, labels = input_parser.parse()
    repositories = map_urls_to_repositories(splitted_urls)

    clf = Classifier.load()

    if not clf:
        response.string_output = 'No trained model available.'
        return response

    samples = extraction_pipeline.extract_features(repositories)
    predict_labels = clf.predict(samples)

    results = []
    for sample, repo, predicted in zip(samples, repositories, predict_labels):
        categories, probabilities = clf.predict_proba([sample])
        out = ValidationEntity()
        out.repo = repo
        out.sample = sample
        out.predicted = predicted
        out.prob = list((category, '{0:.2f}'.format(prob)) for category, prob in zip(categories, probabilities[0]))
        results.append(out)

        result = '{} ({}) - {} \n\t'.format(repo.identifier, repo.category, str(str(repo.category) == predicted))
        result += '\t'.join(
            ['{}: {:.2%}'.format(category, prob) for category, prob in zip(categories, probabilities[0])])
        # results.append(result)

    # First the wrong classifications for view
    results.sort(key=lambda x: x.repo.category == x.predicted)

    evaluator = Evaluator(clf, labels, predict_labels)
    response.string_output += '\n' + evaluator.report()
    response.string_output += '\n' + evaluator.confusion_matrix()
    response.items = results
    return response

    # yield evaluator.report()
    # yield 'Probabilities\n' + '\n'.join(results)
    # yield evaluator.confusion_matrix()


def classify_single_repo(url):
    repo, _ = Repository.objects.get_or_create(url=url, defaults={'url': url})

    clf = Classifier.load()
    if not clf:
        return 'No trained model available.'

    samples = extraction_pipeline.extract_features([repo])
    categories, probabilities = clf.predict_proba(samples)
    result = '\n'.join(['{}: {:.2%}'.format(category, prob) for category, prob in zip(categories, probabilities[0])])

    return result


def map_urls_to_repositories(urls: [str]) -> [Repository]:
    repos = []
    for url in urls:
        repo, created = Repository.objects.get_or_create(url=url, defaults={'url': url})
        repos.append(repo)
    return repos


class Response:
    string_output = ''
    items = []


class ValidationEntity:
    pass
