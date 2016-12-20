from django.db import models


class Repository(models.Model):
    class Meta:
        verbose_name_plural = 'repositories'

    CATEGORIES = (
        ('DEV', 'DEV'),
        ('HW', 'HW'),
        ('EDU', 'EDU'),
        ('DOCS', 'DOCS'),
        ('WEB', 'WEB'),
        ('DATA', 'DATA'),
        ('OTHER', 'OTHER'),
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
