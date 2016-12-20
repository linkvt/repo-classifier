from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from classification.models import Repository


class RepositoryResource(resources.ModelResource):
    class Meta:
        model = Repository
        exclude = ('id',)
        export_order = ('url', 'category')
        import_id_fields = ('url',)
        skip_unchanged = True


class RepositoryAdmin(ImportExportModelAdmin):
    resource_class = RepositoryResource


admin.site.register(Repository, RepositoryAdmin)
