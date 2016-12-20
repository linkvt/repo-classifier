from classification.feature_extraction.CommonFeatureExtractors import BranchExtractor, ContributorsExtractor, \
    ForkExtractor, StarExtractor
from classification.feature_extraction.FeatureCategory import FeatureCategory
from classification.feature_extraction.FeatureExtractor import FeatureExtractor


class MainCategory(FeatureCategory):
    def _get_feature_extractors(self) -> [FeatureExtractor]:
        classes = [
            BranchExtractor,
            ContributorsExtractor,
            ForkExtractor,
            StarExtractor,
        ]

        return [cls(self.repo) for cls in classes]
