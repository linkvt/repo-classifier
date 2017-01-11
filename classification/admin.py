from django.contrib import admin
from import_export import fields
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV
from import_export.widgets import ForeignKeyWidget

from classification.models import Repository, Feature


class CSVKeepingOrder(CSV):
    def create_dataset(self, in_stream, **kwargs):
        # reverse line order, because they get reversed again by the framework when importing them
        lines = in_stream.split('\n')
        header = lines.pop(0)
        lines = list(filter(None, lines))
        in_stream = header + '\n' + '\n'.join(lines[::-1])
        return super(CSV, self).create_dataset(in_stream, **kwargs)


class RepositoryResource(resources.ModelResource):
    class Meta:
        model = Repository
        exclude = ('id',)
        export_order = ('url', 'category')
        import_id_fields = ('url',)
        skip_unchanged = True


class RepositoryAdmin(ImportExportModelAdmin):
    resource_class = RepositoryResource
    formats = (CSVKeepingOrder,)
    list_display = ('url', 'category')
    list_editable = ('category',)
    list_filter = ('category',)
    list_max_show_all = 10000
    search_fields = ('url',)

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
    list_filter = ('repository__category', 'name')
    list_max_show_all = 10000
    search_fields = ('repository__url', 'name')

    def get_export_filename(self, file_format):
        return 'features.{}'.format(file_format.get_extension())


admin.site.register(Repository, RepositoryAdmin)
admin.site.register(Feature, FeatureAdmin)
