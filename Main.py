import argparse

from classifier.DecisionTreeClassifier import DecisionTreeClassifier
from classifier.GithubAuthentification import GithubAuthentification
from classifier.InputParser import InputParser
from classifier.feature_extraction.FeatureExtractionPipeline import FeatureExtractionPipeline

parser = argparse.ArgumentParser(description='Program which analyses github repositories into categories.')
parser.add_argument('-f', '--file', dest="filepath", help='The file location of the input file', nargs='?', required=True,
                    metavar='FILE')
parser.add_argument('-t', '--train', dest="train", help='Specifies the program to train with the given data', action="store_true")

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
        print('<Testing> Read repo name:{} with label {}'.format( current_repo.name, current_label))
        features = FeatureExtractionPipeline(current_repo).extract_features()
        print('Extracted features: ', features)
        samples.append(features)

    clf.fit(samples, labels)
    predicted_label = clf.predict_with_values([[5, 1]])
    print('Prediction: ', predicted_label)
