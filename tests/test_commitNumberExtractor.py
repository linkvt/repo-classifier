from unittest import TestCase

from classifier.feature_extraction.feature.CommitNumberExtractor import CommitNumberExtractor
from tests.GithubInitializerForTest import GithubInitializerForTest


class TestCommitNumberExtractor(TestCase):
    def test_extract_features(self):
        repo = GithubInitializerForTest.get_connection().get_repo('rmccue/test-repository')
        extracted_features = CommitNumberExtractor(repo).extract_features()
        assert len(extracted_features) == 1
        assert extracted_features.pop().value == 3
