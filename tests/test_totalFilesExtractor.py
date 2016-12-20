from unittest import TestCase

from classification.tests.GithubInitializerForTest import GithubInitializerForTest

from classification.feature_extraction.feature.TotalFilesExtractor import TotalFilesExtractor


class TestTotalFilesExtractor(TestCase):
    def test_extract_features(self):
        repo = GithubInitializerForTest.get_connection().get_repo('rmccue/test-repository')
        extracted_features = TotalFilesExtractor(repo).extract_features()
        assert len(extracted_features) == 1
        assert extracted_features.pop().value == 2
