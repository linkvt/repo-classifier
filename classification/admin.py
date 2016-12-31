import tablib
from django.contrib import admin
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV
from import_export.widgets import ForeignKeyWidget

from classification.models import Repository, Feature


class RepositoryResource(resources.ModelResource):
    class Meta:
        model = Repository
        exclude = ('id',)
        export_order = ('url', 'category')
        import_id_fields = ('url',)
        skip_unchanged = True


class CSVForRepository(CSV):
    _column_headers = ['url', 'category']
    _delimiter = ' '

    def create_dataset(self, in_stream: str, **kwargs):
        # reverse line order, because they get reversed again by the framework when importing them
        lines = in_stream.split('\n')
        # filter empty lines
        lines = list(filter(None, lines))
        lines.append(self._delimiter.join(self._column_headers))
        in_stream = '\n'.join(lines[::-1])

        data = tablib.Dataset()
        self.get_format().import_set(data, in_stream, delimiter=self._delimiter, **kwargs)
        return data

    def export_data(self, dataset, **kwargs):
        dataset.headers = []
        return self.get_format().export_set(dataset, delimiter=self._delimiter, **kwargs)


class CSVKeepingOrder(CSV):
    def create_dataset(self, in_stream, **kwargs):
        # reverse line order, because they get reversed again by the framework when importing them
        lines = in_stream.split('\n')
        header = lines.pop(0)
        lines = list(filter(None, lines))
        in_stream = header + '\n' + '\n'.join(lines[::-1])
        return super(CSV, self).create_dataset(in_stream, **kwargs)


class RepositoryAdmin(ImportExportModelAdmin):
    resource_class = RepositoryResource
    formats = (CSVForRepository,)
    list_display = ('url', 'category')
    list_max_show_all = 10000

    def get_export_filename(self, file_format):
        return 'repositories.{}'.format(file_format.get_extension())


class FeatureResource(resources.ModelResource):
    repository = fields.Field(attribute='repository',
                              column_name='repository',
                              widget=ForeignKeyWidget(Repository, 'url'))

    class Meta:
        model = Feature
        fields = ('repository', 'name', 'value')
        export_order = fields
        import_id_fields = ('repository', 'name')
        skip_unchanged = True


class FeatureAdmin(ImportExportModelAdmin):
    resource_class = FeatureResource
    formats = (CSVKeepingOrder,)
    list_display = ('repository', 'name', 'value')
    list_max_show_all = 10000

    def get_export_filename(self, file_format):
        return 'features.{}'.format(file_format.get_extension())


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Feature, FeatureAdmin)
