from sklearn import tree


class DecisionTreeClassifier():
    def __init__(self):
        self.clf = tree.DecisionTreeClassifier()

    def fit(self, samples, labels):
        self.clf = self.clf.fit(samples, labels)

    def predict(self, samples):
        return self.clf.predict(samples)
