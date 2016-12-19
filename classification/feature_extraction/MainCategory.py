from classification.feature_extraction.FeatureCategory import FeatureCategory
from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.feature_extraction.feature.BranchExtractor import BranchExtractor
from classification.feature_extraction.feature.ContributorsExtractor import ContributorsExtractor
from classification.feature_extraction.feature.ForkExtractor import ForkExtractor

from classification.feature_extraction.feature.StarExtractor import StarExtractor


class MainCategory(FeatureCategory):
    def _get_feature_extractors(self) -> [FeatureExtractor]:
        return [ForkExtractor(self.repo), ContributorsExtractor(self.repo), BranchExtractor(self.repo),
                StarExtractor(self.repo)]
