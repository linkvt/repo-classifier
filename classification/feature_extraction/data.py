"""Contains extractors that are used for the DATA category."""
import typing

from classification.feature_extraction.LanguageFeatureExtractor import LanguageFeatureExtractor
from classification.feature_extraction.misc import FileExtensionExtractor
from classification.models import Feature

CATEGORY = 'DATA'


class DATAFileExtensionExtractor(FileExtensionExtractor):
    @property
    def category(self) -> str:
        return CATEGORY

    @property
    def extensions_to_check(self) -> typing.Set[str]:
        font_extensions = {'.otf', '.ttf'}
        return {'.7z', '.json', '.geojson', '.xml', '.csv', '.yml', '.yaml', '.txt', '.sql', '.xls', '.xlsx', '.zip',
                *font_extensions}


class LanguageDATAExtractor(LanguageFeatureExtractor):
    def _init_features(self):
        self.features = [Feature.create('Language feature for ' + CATEGORY)]

    def _get_relevant_languages(self) -> [str]:
        return ['Perl', 'Python', 'R', 'Ruby', 'Shell']
