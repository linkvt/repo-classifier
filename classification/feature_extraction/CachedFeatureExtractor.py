from typing import Union

from classification.feature_extraction import FeatureExtractor
from classification.models import Feature, Repository


class CachedFeatureExtractor:
    def __init__(self, extractor: FeatureExtractor):
        self.extractor = extractor

    def extract_features(self) -> [Feature]:
        for feature in self.extractor.features:
            cached_feature = self.get_cached(self.extractor.repo, feature)
            if cached_feature:
                feature.value = cached_feature.value
            else:
                new_features = self.extractor.extract_features()
                for new_feature in new_features:
                    self.update_cached(self.extractor.repo, new_feature)
                return new_features

        return self.extractor.features

    def get_cached(self, repo: Repository, feature: Feature) -> Union[Feature, None]:
        try:
            feature = Feature.objects.get(repository=repo, name=feature.name)
            return feature
        except Feature.DoesNotExist:
            return None

    def update_cached(self, repo: Repository, feature: Feature):
        repo.feature_set.update_or_create(name=feature.name, defaults={'value': feature.value})
