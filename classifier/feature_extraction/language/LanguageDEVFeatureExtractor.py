from classifier.feature_extraction.language.LanguageFeatureExtractor import LanguageFeatureExtractor


class LanguageDEVFeatureExtractor(LanguageFeatureExtractor):
    def __get_relevant_languages__(self) -> [str]:
        return ['Python', 'Java']

    def __get_category_label__(self) -> str:
        return 'DEV'
