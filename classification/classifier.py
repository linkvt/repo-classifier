from sklearn.model_selection import train_test_split

from classification.GithubAuthentification import GithubAuthentification
from classification.InputParser import InputParser
from classification.algorithm.algorithms import Classifier, DecisionTreeClassifier, KNeighborsClassifier, MLPClassifier
from classification.evaluation.Evaluator import Evaluator
from classification.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline


def train(text, train=True):
    github_connection = GithubAuthentification()

    input_parser = InputParser(text, train)
    splitted_urls, labels = input_parser.parse()

    classifiers = [DecisionTreeClassifier(), MLPClassifier(), KNeighborsClassifier()]

    if train:
        samples = []

        # build the samples
        for (url, current_label) in zip(splitted_urls, labels):
            current_repo = github_connection.get_repo(url)
            print('<Testing> Read repo name:{} with label {}'.format(current_repo.name, current_label))
            features = FeatureExtractionPipeline(current_repo).extract_features()
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
    GITHUB_PREFIX = 'https://github.com/'
    github_connection = GithubAuthentification()

    input_parser = InputParser(text, train)
    urls, _ = input_parser.parse()

    clf = Classifier.load()

    if not clf:
        yield 'No trained model available.'
        return

    samples = []

    for url in urls:
        current_repo = github_connection.get_repo(url)
        print('<Testing> Read repo name:{}'.format(current_repo.name))
        features = FeatureExtractionPipeline(current_repo).extract_features()
        print('Extracted features: ', str(features))
        samples.append(features)

    labels = clf.predict(samples)

    result = [GITHUB_PREFIX + url + ' ' + label for url, label in zip(urls, labels)]

    for r in result:
        yield r
