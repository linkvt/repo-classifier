def setup():
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repo_classifier.settings")
    import django
    django.setup()
