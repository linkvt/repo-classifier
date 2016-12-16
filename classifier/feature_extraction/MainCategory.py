from classifier.feature_extraction.feature.ContributorsExtractor import ContributorsExtractor
from classifier.feature_extraction.feature.ForkExtractor import ForkExtractor
from classifier.feature_extraction.FeatureCategory import FeatureCategory
from classifier.feature_extraction.FeatureExtractor import FeatureExtractor


class MainCategory(FeatureCategory):
    def _get_feature_extractors(self) -> [FeatureExtractor]:
        return [ForkExtractor(self.repo), ContributorsExtractor(self.repo)]
