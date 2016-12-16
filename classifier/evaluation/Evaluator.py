from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report


class Evaluator:
    def __init__(self, test_labels, predict_labels):
        self.test_labels = test_labels
        self.predict_labels = predict_labels

    def accuracy(self):
        return accuracy_score(self.test_labels, self.predict_labels, normalize=True)

    def f1(self):
        return f1_score(self.test_labels, self.predict_labels, average=None)

    def report(self):
        acc = 'Accuracy: {:.2%}'.format(self.accuracy())
        f1 = 'F1-Score: {}'.format([score for score in self.f1()])
        report = classification_report(self.test_labels, self.predict_labels)

        return '\n'.join([acc, f1, report])
