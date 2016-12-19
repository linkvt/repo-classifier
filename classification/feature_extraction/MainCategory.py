from classification.feature_extraction.FeatureCategory import FeatureCategory
from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.feature_extraction.feature.BranchExtractor import BranchExtractor
from classification.feature_extraction.feature.ContributorsExtractor import ContributorsExtractor
from classification.feature_extraction.feature.ForkExtractor import ForkExtractor
from classification.feature_extraction.feature.StarExtractor import StarExtractor


class MainCategory(FeatureCategory):
    def _get_feature_extractors(self) -> [FeatureExtractor]:
        classes = [
            BranchExtractor,
            ContributorsExtractor,
            ForkExtractor,
            StarExtractor,
        ]

        return [cls(self.repo) for cls in classes]
