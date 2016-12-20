from collections import namedtuple

from django.db import models

Category = namedtuple('Category', ['name', 'label'])


class Repository(models.Model):
    class Meta:
        verbose_name_plural = 'repositories'

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

    def get_identifier(self):
        return self.url[19:]  # TODO refactor other places which use this code

    def __str__(self):
        readable_name = self.get_identifier()
        if self.category:
            readable_name += ' ({})'.format(self.category)
        return readable_name
