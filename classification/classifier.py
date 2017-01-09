import logging

from sklearn.model_selection import train_test_split

from classification.InputParser import InputParser
from classification.algorithm.algorithms import Classifier, RandomForestClassifier, KNeighborsClassifier, MLPClassifier
from classification.evaluation.Evaluator import Evaluator
from classification.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline
from classification.models import Repository

logger = logging.getLogger(__name__)
extraction_pipeline = FeatureExtractionPipeline()


def train(text, train=True):
    input_parser = InputParser(text, train)
    splitted_urls, labels = input_parser.parse()
    repositories = map_urls_to_repositories(splitted_urls)

    classifiers = [RandomForestClassifier(), MLPClassifier(), KNeighborsClassifier()]

    if train:
        samples = extraction_pipeline.extract_features(repositories)

        training_split = 0.4
        logger.info('Splitting into {:.0%} training and {:.0%} test data.'.format(1 - training_split, training_split))
        train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels,
                                                                                  test_size=training_split,
                                                                                  random_state=0)
        for clf in classifiers:
            clf.fit(train_samples, train_labels)
            predict_labels = clf.predict(test_samples)

            evaluator = Evaluator(clf, test_labels, predict_labels)
            yield evaluator.report()  # TODO return the classified repos when they are associated to the features

        classifiers[0].save()


def classify(text):
    input_parser = InputParser(text, train=False)
    urls, _ = input_parser.parse()
    repos = map_urls_to_repositories(urls)

    clf = Classifier.load()

    if not clf:
        yield 'No trained model available.'
        return

    samples = extraction_pipeline.extract_features(repos)

    labels = clf.predict(samples)

    result = [url + ' ' + label for url, label in zip(urls, labels)]

    for r in result:
        yield r


def classify_single_repo(url):
    repo, _ = Repository.objects.get_or_create(url=url, defaults={'url': url})

    clf = Classifier.load()
    if not clf:
        yield 'No trained model available.'
        return

    samples = extraction_pipeline.extract_features([repo])
    categories, probabilities = clf.predict_proba(samples)
    result = '\n'.join(['{}: {}'.format(category, prob) for category, prob in zip(categories, probabilities[0])])

    yield result


def map_urls_to_repositories(urls: [str]) -> [Repository]:
    repos = []
    for url in urls:
        repo, created = Repository.objects.get_or_create(url=url, defaults={'url': url})
        repos.append(repo)
    return repos
