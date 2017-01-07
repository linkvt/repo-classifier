"""Contains extractors that are used for the DATA category."""
import typing

from classification.feature_extraction.misc import FileExtensionExtractor

CATEGORY = 'DATA'


class DATAFileExtensionExtractor(FileExtensionExtractor):
    @property
    def category(self) -> str:
        return CATEGORY

    @property
    def extensions_to_check(self) -> typing.Set[str]:
        return {'.json', '.xml', '.csv', '.yml', '.txt', '.sql', '.xls', '.xlsx'}
