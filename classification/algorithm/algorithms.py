from sklearn import neighbors
from sklearn import tree
from sklearn import neural_network
from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler


class Classifier:
    model_file_name = 'model.pkl'

    def __init__(self, clf, name):
        self.clf = clf
        self.name = name
        self.scaler = StandardScaler()

    def fit(self, samples, labels):
        """
        samples eq. -> [[Feature1, Feature2], [Feature1, Feature2]]
        :param samples:
        :param labels:
        :return:
        """
        feature_vectors = self._map_input(samples)
        scaled_vectors = self.scaler.fit_transform(feature_vectors)
        self.clf = self.clf.fit(scaled_vectors, labels)

    def predict(self, samples):
        """
        The sample input contains only the necessary values for scikit input
        :param samples:
        :return:
        """
        feature_vectors = self._map_input(samples)
        scaled_vectors = self.scaler.transform(feature_vectors)
        return self.clf.predict(scaled_vectors)

    def predict_with_values(self, samples):
        return self.clf.predict(self.scaler.transform(samples))

    def save(self):
        joblib.dump(self, self.model_file_name)

    @staticmethod
    def load():
        try:
            return joblib.load(Classifier.model_file_name)
        except FileNotFoundError:
            return None

    def _map_input(self, samples):
        """
        We need a specific input for the scikit classifier
        :param samples:
        :return:
        """
        return [[feature.value for feature in sample] for sample in samples]


class DecisionTreeClassifier(Classifier):
    def __init__(self):
        super().__init__(tree.DecisionTreeClassifier(), 'DecisionTreeClassifier')


class KNeighborsClassifier(Classifier):
    def __init__(self):
        super().__init__(neighbors.KNeighborsClassifier(5), 'KNeighborsClassifier')


class MLPClassifier(Classifier):
    def __init__(self):
        super().__init__(neural_network.MLPClassifier(), 'MLPClassifier')
