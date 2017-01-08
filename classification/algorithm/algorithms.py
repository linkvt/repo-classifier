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

    def __init__(self, clf, params, name):
        self.clf = Pipeline([('kbest', SelectKBest()), ('clf', clf)])
        params['kbest__k'] = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 'all']
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
        print('Best Params:')
        print(self.clf.best_params_)

    def predict(self, samples):
        """
        The sample input contains only the necessary values for scikit input
        :param samples:
        :return:
        """
        feature_vectors = self._map_input(samples)
        scaled_vectors = self.scaler.transform(feature_vectors)
        return self.clf.predict(scaled_vectors)

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
        params = dict(clf__n_estimators=[5, 10, 15, 20])
        super().__init__(ensemble.RandomForestClassifier(), params, 'RandomForestClassifier')


class KNeighborsClassifier(Classifier):
    def __init__(self):
        params = dict(clf__n_neighbors=[2, 4, 6, 8])
        super().__init__(neighbors.KNeighborsClassifier(), params, 'KNeighborsClassifier')


class MLPClassifier(Classifier):
    def __init__(self):
        params = dict(clf__hidden_layer_sizes=[(80,), (100,), (120,)], clf__solver=['lbfgs', 'adam', 'sgd'])
        super().__init__(neural_network.MLPClassifier(), params, 'MLPClassifier')
