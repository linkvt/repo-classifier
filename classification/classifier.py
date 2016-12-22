from sklearn.model_selection import train_test_split

from classification.GithubAuthentification import GithubAuthentification
from classification.InputParser import InputParser
from classification.algorithm.DecisionTreeClassifier import DecisionTreeClassifier
from classification.evaluation.Evaluator import Evaluator
from classification.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline


def train_and_classify(filepath, train=True):
    github_connection = GithubAuthentification()

    input_parser = InputParser(filepath, train)
    splitted_urls, labels = input_parser.parse()

    clf = DecisionTreeClassifier()

    if train:
        samples = []

        # build the samples
        for (url, current_label) in zip(splitted_urls, labels):
            current_repo = github_connection.get_repo(url)
            yield '<Testing> Read repo name:{} with label {}'.format(current_repo.name, current_label)
            features = FeatureExtractionPipeline(current_repo).extract_features()
            yield 'Extracted features: ' + str(features)
            samples.append(features)

        training_split = 0.2
        yield 'Splitting the data into {:.0%} training and {:.0%} test data.'.format(1 - training_split, training_split)
        train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels, test_size=0.2,
                                                                                  random_state=0)
        clf.fit(train_samples, train_labels)
        predict_labels = clf.predict(test_samples)

        evaluator = Evaluator(test_labels, predict_labels)
        yield evaluator.report()
