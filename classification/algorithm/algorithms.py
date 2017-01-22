from sklearn import ensemble
from sklearn import neighbors
from sklearn import neural_network
from sklearn import svm
from sklearn.externals import joblib
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import mutual_info_classif
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


class Classifier:
    model_file_name = 'model.pkl'

    def __init__(self, clf, params, name):
        self.clf = Pipeline([('select', SelectPercentile(score_func=mutual_info_classif, percentile=70)), ('clf', clf)])
        params['select__percentile'] = [50, 60, 70, 80, 90]
        self.clf = GridSearchCV(self.clf, param_grid=params, scoring='f1_macro')
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
        feature_names = [feature.name for feature in samples[0]]
        scaled_vectors = self.scaler.fit_transform(feature_vectors)
        self.clf = self.clf.fit(scaled_vectors, labels)

        if hasattr(self.clf.best_estimator_.named_steps['clf'], 'feature_importances_'):
            feature_indices = self.clf.best_estimator_.named_steps['select'].get_support(indices=True)
            selected_features = [feature_names[i] for i in feature_indices]
            feature_importances = self.clf.best_estimator_.named_steps['clf'].feature_importances_
            feature_tuples = [(feature, importance) for feature, importance in
                              zip(selected_features, feature_importances)]
            sorted_features = sorted(feature_tuples, key=lambda t: t[1], reverse=True)

            for name, importance in sorted_features:
                print("Feature {}: {}".format(name, importance))

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

    def predict_proba(self, samples):
        feature_vectors = self._map_input(samples)
        scaled_vectors = self.scaler.transform(feature_vectors)
        return self.clf.best_estimator_.named_steps['clf'].classes_, self.clf.predict_proba(scaled_vectors)

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
        params = dict(clf__n_estimators=[60, 80, 100], clf__min_samples_split=[2], clf__max_depth=[None, 30, 40])
        class_weights = {'DEV': 1, 'WEB': 2, 'DATA': 4, 'DOCS': 4, 'EDU': 15, 'HW': 5, 'OTHER': 10}
        super().__init__(ensemble.RandomForestClassifier(class_weight=class_weights), params, 'RandomForestClassifier')


class ExtraTreesClassifier(Classifier):
    def __init__(self):
        params = dict(clf__n_estimators=[60, 80, 100], clf__min_samples_split=[2], clf__max_depth=[None, 30, 40])
        class_weights = {'DEV': 1, 'WEB': 2, 'DATA': 4, 'DOCS': 4, 'EDU': 15, 'HW': 5, 'OTHER': 10}
        super().__init__(ensemble.ExtraTreesClassifier(class_weight=class_weights), params, 'ExtraTreesClassifier')


class KNeighborsClassifier(Classifier):
    def __init__(self):
        params = dict(clf__n_neighbors=[2, 4, 6, 8, 10])
        super().__init__(neighbors.KNeighborsClassifier(), params, 'KNeighborsClassifier')


class SVMClassifier(Classifier):
    def __init__(self):
        params = dict(clf__kernel=['linear', 'rbf', 'poly'])
        super().__init__(svm.SVC(class_weight='balanced', probability=True), params, 'SVMClassifier')


class MLPClassifier(Classifier):
    def __init__(self):
        params = dict(clf__hidden_layer_sizes=[(50,), (70,), (100,)], clf__solver=['lbfgs', 'adam', 'sgd'])
        super().__init__(neural_network.MLPClassifier(), params, 'MLPClassifier')
