from classification.feature_extraction.language.LanguageFeatureExtractor import LanguageFeatureExtractor


class LanguageDEVFeatureExtractor(LanguageFeatureExtractor):
    def _get_relevant_languages(self) -> [str]:
        return ['Python', 'Java']

    def _get_category_label(self) -> str:
        return 'DEV'
