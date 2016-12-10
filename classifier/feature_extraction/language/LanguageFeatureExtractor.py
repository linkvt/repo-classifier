from classifier.Feature import Feature
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor


class LanguageFeatureExtractor(FeatureExtractor):
    """
    The languages returned from github are mapped to the kb size of usage.
    Eq {'Python': 98564, 'R': 4914}
    """

    def extract_feature(self) -> Feature:
        languages = self.repo.get_languages()
        total_size = sum(languages.values())
        relevant_size = 0

        for language in self.__get_relevant_languages__():
            if language in languages:
                relevant_size += languages[language]

        return Feature('Language feature for DEV', relevant_size / total_size)

    def __get_relevant_languages__(self):
        return ['Python', 'Java']
