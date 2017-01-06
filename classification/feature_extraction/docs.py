"""Contains extractors that are used for the DOCS category."""
import typing

from classification.feature_extraction.misc import FileExtensionExtractor

CATEGORY = 'DOCS'


class DOCSFileExtensionExtractor(FileExtensionExtractor):
    @property
    def category(self) -> str:
        return CATEGORY

    @property
    def extensions_to_check(self) -> typing.Set[str]:
        return {'.md'}
