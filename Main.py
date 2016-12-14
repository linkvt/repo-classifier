import argparse

from sklearn.model_selection import train_test_split

from classifier.algorithm.DecisionTreeClassifier import DecisionTreeClassifier
from classifier.GithubAuthentification import GithubAuthentification
from classifier.InputParser import InputParser
from classifier.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline

from classifier.evaluation.Evaluator import Evaluator

parser = argparse.ArgumentParser(description='Program which analyses github repositories into categories.')
parser.add_argument('-f', '--file', dest="filepath", help='The file location of the input file', nargs='?',
                    required=True,
                    metavar='FILE')
parser.add_argument('-t', '--train', dest="train", help='Specifies the program to train with the given data',
                    action="store_true")

args = parser.parse_args()

github_connection = GithubAuthentification()

input_parser = InputParser(args.filepath, args.train)
splitted_urls, labels = input_parser.parse()

clf = DecisionTreeClassifier()

if args.train:
    samples = []

    # build the samples
    for (url, current_label) in zip(splitted_urls, labels):
        current_repo = github_connection.get_repo(url)
        print('<Testing> Read repo name:{} with label {}'.format(current_repo.name, current_label))
        features = FeatureExtractionPipeline(current_repo).extract_features()
        print('Extracted features: ', features)
        samples.append(features)

    training_split = 0.2
    print('Splitting the data into {:.0%} training and {:.0%} test data.'.format(1 - training_split, training_split))
    train_samples, test_samples, train_labels, test_labels = train_test_split(samples, labels, test_size=0.2,
                                                                              random_state=0)
    clf.fit(train_samples, train_labels)
    predict_labels = clf.predict(test_samples)

    evaluator = Evaluator(test_labels, predict_labels)
    print(evaluator.report())


