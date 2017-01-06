import abc

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class LanguageFeatureExtractor(FeatureExtractor):
    """
    The languages returned from github are mapped to the byte size of usage.
    Eq {'Python': 98564, 'R': 4914}
    """

    def _extract(self) -> [Feature]:
        languages = self.api_repo.get_languages()
        total_size = sum(languages.values())
        relevant_size = 0

        for language in self._get_relevant_languages():
            if language in languages:
                relevant_size += languages[language]

        self.features[0].value = relevant_size / total_size if total_size > 0 else 0

    @abc.abstractmethod
    def _get_relevant_languages(self) -> [str]:
        raise NotImplementedError('Should be implemented in subclasses!')
