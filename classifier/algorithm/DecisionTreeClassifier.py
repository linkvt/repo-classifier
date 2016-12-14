from sklearn import tree


class DecisionTreeClassifier():
    def __init__(self):
        self.clf = tree.DecisionTreeClassifier()

    def fit(self, samples, labels):
        """
        samples eq. -> [[Feature1, Feature2], [Feature1, Feature2]]
        :param samples:
        :param labels:
        :return:
        """
        self.clf = self.clf.fit(self._map_input(samples), labels)

    def predict(self, samples):
        """
        The sample input contains only the necessary values for scikit input
        :param samples:
        :return:
        """
        return self.clf.predict(self._map_input(samples))

    def predict_with_values(self, samples):
        return self.clf.predict(samples)

    def _map_input(self, samples):
        """
        We need a specific input for the scikit classifier
        :param samples:
        :return:
        """
        return [[feature.value for feature in sample] for sample in samples]
