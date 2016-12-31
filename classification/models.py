from collections import namedtuple

from django.db import models

Category = namedtuple('Category', ['name', 'label'])


class Repository(models.Model):
    class Meta:
        verbose_name_plural = 'repositories'
        app_label = 'classification'  # Hot fix for error during testing

    CATEGORIES = (
        Category('DEV', 'DEV'),
        Category('HW', 'HW'),
        Category('EDU', 'EDU'),
        Category('DOCS', 'DOCS'),
        Category('WEB', 'WEB'),
        Category('DATA', 'DATA'),
        Category('OTHER', 'OTHER'),
    )

    url = models.CharField(max_length=255, unique=True)
    category = models.CharField(max_length=10, blank=True, choices=CATEGORIES)

    @property
    def identifier(self):
        return self.url[19:]

    @property
    def name(self):
        return self.url.rsplit('/', 1)[-1]

    def __str__(self):
        readable_name = self.identifier
        if self.category:
            readable_name += ' ({})'.format(self.category)
        return readable_name


class Feature(models.Model):
    class Meta:
        unique_together = ('repository', 'name')
        app_label = 'classification'  # Hot fix see above

    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return 'Feature[' + self.name + ', ' + str(self.value) + ']'

    def __repr__(self):
        return self.__str__()
