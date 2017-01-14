from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics.classification import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support


class Evaluator:
    categories = ['DEV', 'WEB', 'DATA', 'DOCS', 'EDU', 'HW', 'OTHER']

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
        return str(self.categories) + '\n' + str(
            confusion_matrix(self.test_labels, self.predict_labels, labels=self.categories))

    def confusion_matrix_raw(self):
        return confusion_matrix(self.test_labels, self.predict_labels, labels=self.categories).tolist()

    def report_raw(self):
        precision, recall, f1, support = precision_recall_fscore_support(self.test_labels, self.predict_labels,
                                                                         labels=self.categories)
        prec_average, rec_average, f1_average, _ = precision_recall_fscore_support(self.test_labels,
                                                                                            self.predict_labels,
                                                                                            average='macro',
                                                                                            labels=self.categories)
        support_total = sum(support)
        matrix = [precision.tolist(), recall.tolist(), f1.tolist(), support.tolist()]
        matrix = [list(i) for i in zip(*matrix)]
        matrix.append([prec_average, rec_average, f1_average, support_total])
        return matrix
