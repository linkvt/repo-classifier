from sklearn import ensemble
from sklearn import neighbors
from sklearn import neural_network
from sklearn.externals import joblib
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


class Classifier:
    model_file_name = 'model.pkl'

    def __init__(self, clf, name):
        self.clf = Pipeline([('kbest', SelectKBest(k=25)), ('clf', clf)])
        params = dict(kbest__k=[10, 15, 20, 25, 30])
        self.clf = GridSearchCV(self.clf, param_grid=params)
        self.name = name
        self.scaler = MinMaxScaler()

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


class RandomForestClassifier(Classifier):
    def __init__(self):
        super().__init__(ensemble.RandomForestClassifier(n_estimators=10), 'RandomForestClassifier')


class KNeighborsClassifier(Classifier):
    def __init__(self):
        super().__init__(neighbors.KNeighborsClassifier(5), 'KNeighborsClassifier')


class MLPClassifier(Classifier):
    def __init__(self):
        super().__init__(neural_network.MLPClassifier(), 'MLPClassifier')
