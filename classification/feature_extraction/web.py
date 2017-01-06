from classification.feature_extraction.LanguageFeatureExtractor import LanguageFeatureExtractor
from classification.models import Feature


class LanguageWEBExtractor(LanguageFeatureExtractor):
    def _init_features(self):
        self.features = [Feature.create('Language feature for WEB')]

    def _get_relevant_languages(self) -> [str]:
        return ["HTML", "JavaScript", "CSS", "Ruby", "PostScript", "PHP"]
