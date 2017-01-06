from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.feature_extraction.LanguageFeatureExtractor import LanguageFeatureExtractor
from classification.models import Feature


class LanguageWEBExtractor(LanguageFeatureExtractor):
    def _init_features(self):
        self.features = [Feature.create('Language feature for WEB')]

    def _get_relevant_languages(self) -> [str]:
        return ["HTML", "JavaScript", "CSS", "Ruby", "PostScript", "PHP"]


class DescriptionContainsURLExtractor(FeatureExtractor):
    def _init_features(self):
        self.features = [Feature.create("Description contains URL")]

    def _extract(self):
        self.features[0].value = 1 if self.api_repo.homepage else 0
