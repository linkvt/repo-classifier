"""Contains extractors that belong to no specific category but can be used in multiple categories."""

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.models import Feature


class DescriptionKeyWordExtractor(FeatureExtractor):
    # TODO: Add more keywords
    keywords = ['homework', 'lecture', 'course', 'framework', 'assignment', 'application', 'api', 'webapp', 'icons',
                'data', 'list', 'fonts', 'materials', 'introduction', 'github', 'website', 'site', 'page', 'assignment',
                'group', 'official', 'documentation', 'document', 'dokument', 'policy']

    def _init_features(self):
        self.features = [Feature(name='Contains keyword "' + keyword + '"') for keyword in self.keywords]

    def _extract(self):
        description = self.api_repo.description.lower() if self.api_repo.description else ''

        for keyword, feature in zip(self.keywords, self.features):
            if keyword in description:
                feature.value = 1
            else:
                feature.value = 0
