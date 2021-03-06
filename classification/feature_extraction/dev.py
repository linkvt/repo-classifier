"""Contains extractors that are used for the DEV category."""

from github import GithubException

from classification.feature_extraction.FeatureExtractor import FeatureExtractor
from classification.feature_extraction.LanguageFeatureExtractor import LanguageFeatureExtractor
from classification.models import Feature


class HasBuildFileExtractor(FeatureExtractor):
    # TODO: Add more build files
    build_files = ['.travis.yml', 'appveyor.yml', 'circle.yml', 'CMakeLists.txt', 'cmake', 'tox.ini', 'setup.py',
                   'build.gradle', 'gradle', 'gradlew', 'composer.json', 'Makefile', 'package.json', 'pom.xml',
                   'requirements.txt', 'manifest.json', 'Package.swift']

    def _init_features(self):
        self.feature = Feature.create('Has build file')

    def _extract(self):
        try:
            files = self.api_repo.get_dir_contents('')
        except GithubException:
            files = []

        self.feature.value = 0
        for file in files:
            if file.name and file.name.lower() in self.build_files:
                self.feature.value = 1


class LanguageDEVExtractor(LanguageFeatureExtractor):
    def _init_features(self):
        self.features = [Feature.create('Language feature for DEV')]

    def _get_relevant_languages(self) -> [str]:
        return ["C++", "Python", "C", "Java", "JavaScript", "Go", "C#", "Rust", "FORTRAN", "Swift", "CMake", "Perl",
                "Scala", "Pascal", "Objective-C", "Assembly", "Clojure", "Smalltalk"]
