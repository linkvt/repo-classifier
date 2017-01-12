from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics.classification import confusion_matrix


class Evaluator:
    def __init__(self, clf, test_labels, predict_labels):
        self.clf = clf
        self.test_labels = test_labels
        self.predict_labels = predict_labels

    def accuracy(self):
        return accuracy_score(self.test_labels, self.predict_labels, normalize=True)

    def f1(self):
        return f1_score(self.test_labels, self.predict_labels, average=None)

    def report(self):
        report = classification_report(self.test_labels, self.predict_labels)

        return self.clf.name + '\n' + report

    def confusion_matrix(self):
        legend = ['DEV', 'WEB', 'DATA', 'DOCS', 'EDU', 'HW', 'OTHER']
        return str(legend) + '\n' + str(confusion_matrix(self.test_labels, self.predict_labels, labels=legend))
