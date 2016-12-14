from classifier.feature_extraction.ForkExtractor import ForkExtractor
from classifier.feature_extraction.FeatureCategory import FeatureCategory
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor
from classifier.feature_extraction.language.AllLanguageFeatureExtractor import AllLanguageFeatureExtractor
from classifier.feature_extraction.language.LanguageDEVFeatureExtractor import LanguageDEVFeatureExtractor


class MainCategory(FeatureCategory):
    def _get_feature_extractors(self) -> [FeatureExtractor]:
        return [ForkExtractor(self.repo), LanguageDEVFeatureExtractor(self.repo)]
