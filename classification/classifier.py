from typing import List

from sklearn.model_selection import train_test_split

from classification.InputParser import InputParser
from classification.algorithm.algorithms import Classifier, RandomForestClassifier, KNeighborsClassifier, MLPClassifier
from classification.evaluation.Evaluator import Evaluator
from classification.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline
from classification.models import Repository


def train(text, train=True):
    input_parser = InputParser(text, train)
    splitted_urls, labels = input_parser.parse()
    repositories = map_urls_to_repositories(splitted_urls)

    classifiers = [RandomForestClassifier(), MLPClassifier(), KNeighborsClassifier()]

    if train:
        samples = []

        # build the samples
        with FeatureExtractionPipeline() as extraction_pipeline:
            for (repo, current_label) in zip(repositories, labels):
                print('<Testing> Read repo name:{} with label {}'.format(repo.name, current_label))
                features = extraction_pipeline.extract_features(repo)
                print('Extracted features: ', str(features))
                samples.append(features)

        training_split = 0.5
        print(
            'Splitting the data into {:.0%} training and {:.0%} test data.'.format(1 - training_split, training_split))
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

    samples = []

    with FeatureExtractionPipeline() as extraction_pipeline:
        for repo in repos:
            print('<Testing> Read repo name:{}'.format(repo.name))
            features = extraction_pipeline.extract_features(repo)
            print('Extracted features: ', str(features))
            samples.append(features)

    labels = clf.predict(samples)

    result = [url + ' ' + label for url, label in zip(urls, labels)]

    for r in result:
        yield r


def map_urls_to_repositories(urls: List[str]) -> List[Repository]:
    repos = []
    for url in urls:
        repo, created = Repository.objects.get_or_create(url=url, defaults={'url': url})
        repos.append(repo)
    return repos
