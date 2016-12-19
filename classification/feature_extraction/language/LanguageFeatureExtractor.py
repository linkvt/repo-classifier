import abc

from classification.Feature import Feature
from classification.feature_extraction import FeatureExtractor


class LanguageFeatureExtractor(FeatureExtractor):
    """
    The languages returned from github are mapped to the byte size of usage.
    Eq {'Python': 98564, 'R': 4914}
    """

    def extract_features(self) -> [Feature]:
        languages = self._repo.get_languages()
        total_size = sum(languages.values())
        relevant_size = 0

        for language in self._get_relevant_languages():
            if language in languages:
                relevant_size += languages[language]

        return [Feature('Language feature for ' + self._get_category_label(),
                        relevant_size / total_size if total_size > 0 else 0)]

    @abc.abstractmethod
    def _get_category_label(self) -> str:
        raise NotImplementedError('Should be implemented in subclasses!')

    @abc.abstractmethod
    def _get_relevant_languages(self) -> [str]:
        raise NotImplementedError('Should be implemented in subclasses!')
