# Must be before any model related call or anything
from utils import django_init
django_init.setup()

import argparse

from classification import classifier

parser = argparse.ArgumentParser(description='Program which analyses github repositories into categories.')
parser.add_argument('-f', '--file', dest="filepath", help='The file location of the input file', nargs='?',
                    required=True,
                    metavar='FILE')
parser.add_argument('-t', '--train', dest="train",
                    help='Specifies that training and evaluation should be performed on the given input file',
                    action="store_true")
parser.add_argument('-c', '--classify', dest="classify",
                    help='Specifies that classification should be performed on the given input file',
                    action="store_true")

args = parser.parse_args()

with open(args.filepath) as file:
    text = file.read()

if args.train:
    result = list(classifier.train(text))
    print('\n'.join(result))
elif args.classify:
    result = list(classifier.classify(text))
    print('\n'.join(result))
