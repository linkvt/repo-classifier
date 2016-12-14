import yaml
from github.Repository import Repository

from classifier.Feature import Feature
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor


class AllLanguageFeatureExtractor(FeatureExtractor):
    """
    The languages returned from github are mapped to the byte size of usage.
    Eq {'Python': 98564, 'R': 4914}
    Currently there are 223 languages
    """
    LANGUAGES = []

    def __init__(self, repo: Repository):
        super().__init__(repo)
        self._init_languages()
        self._languageToProbability = {el: 0 for el in AllLanguageFeatureExtractor.LANGUAGES}

    def _init_languages(self):
        if not AllLanguageFeatureExtractor.LANGUAGES:
            with open('languages.yml', 'r') as f:
                doc = yaml.load(f)
                AllLanguageFeatureExtractor.LANGUAGES = [language for language in doc]

    def dict(self):
        return self._languageToProbability

    def extract_features(self) -> [Feature]:
        languages = self._repo.get_languages()
        total_size = sum(languages.values())

        for language in languages:
            if language in self._languageToProbability:
                self._languageToProbability[language] = languages[language] / total_size if total_size > 0 else 0
            else:
                print('Language "' + language + '" is not registered in the algorithm.')

        return [Feature('Language: ' + key, value) for key, value in self._languageToProbability.items()]
