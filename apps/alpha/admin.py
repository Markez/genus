# Register your models here.
import csv

from django.contrib import admin
from django.http import HttpResponse
from rangefilter.filter import DateRangeFilter

from .models import Chama, plan_packages


# function for exporting to csv
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(Chama)
class CreateChamaAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    date_hierarchy = 'date'
    search_fields = ('name', 'creator')
    list_filter = ['contribution_intervals', 'plan_package', ("date", DateRangeFilter)]
    list_display = ['creator', 'mobile_number', 'name', 'year_founded', 'maximum_members', 'contribution_intervals',
                    'total_contributions', 'saved_amounts', 'plan_package']


@admin.register(plan_packages)
class PlanPackagesAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    date_hierarchy = 'date'
    search_fields = ('name', "maximum_users", )
    list_filter = ["name", "maximum_users", ("date", DateRangeFilter)]
    list_display = ["name", "chargable", "charges", "maximum_users", "bulk_emails", "bulk_sms", "slug", "date"]
