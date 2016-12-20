import tablib
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV

from classification.models import Repository


class RepositoryResource(resources.ModelResource):
    class Meta:
        model = Repository
        exclude = ('id',)
        export_order = ('url', 'category')
        import_id_fields = ('url',)
        skip_unchanged = True


class CSVWithSpaces(CSV):
    _column_headers = ['url', 'category']
    _delimiter = ' '

    def create_dataset(self, in_stream, **kwargs):
        in_stream = self._delimiter.join(self._column_headers) + '\n' + in_stream
        data = tablib.Dataset()
        self.get_format().import_set(data, in_stream, delimiter=self._delimiter, **kwargs)
        return data

    def export_data(self, dataset, **kwargs):
        dataset.headers = []
        return self.get_format().export_set(dataset, delimiter=self._delimiter, **kwargs)


class RepositoryAdmin(ImportExportModelAdmin):
    resource_class = RepositoryResource
    formats = (CSVWithSpaces,)

    def get_export_filename(self, file_format):
        return 'repositories.{}'.format(file_format.get_extension())


admin.site.register(Repository, RepositoryAdmin)
