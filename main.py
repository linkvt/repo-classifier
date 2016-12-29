import argparse

from classification import classifier

parser = argparse.ArgumentParser(description='Program which analyses github repositories into categories.')
parser.add_argument('-f', '--file', dest="filepath", help='The file location of the input file', nargs='?',
                    required=True,
                    metavar='FILE')
parser.add_argument('-t', '--train', dest="train", help='Specifies the program to train with the given data',
                    action="store_true")

args = parser.parse_args()

with open(args.filepath) as file:
    text = file.read()

classifier.train(text, args.train)
