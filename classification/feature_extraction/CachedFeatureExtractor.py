from classification.feature_extraction import FeatureExtractor
from classification.models import Feature


class CachedFeatureExtractor:
    def __init__(self, extractor: FeatureExtractor):
        self.extractor = extractor

    def extract_features(self) -> [Feature]:
        for feature in self.extractor.features:
            if not TEST().get_value(self.extractor.repo.url, feature.name):
                new_features = self.extractor.extract_features()
                for new_feature in new_features:
                    TEST().save_values(self.extractor.repo.url, new_feature.name, new_feature.value)
                return new_features
            else:
                feature.value = TEST().get_value(self.extractor.repo.url, feature.name)

        return self.extractor.features


# TODO auslagern
class TEST:
    def _build_cache(self):
        return

    def get_value(self, repo_url, feature_name) -> float:
        return None

    def save_values(self, repo_url, feature_name, value):
        return None
