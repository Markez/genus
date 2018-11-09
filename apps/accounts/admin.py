# Register your models here.
import csv

from django.contrib import admin
from django.http import HttpResponse
from rangefilter.filter import DateRangeFilter

from .models import activation_data, profile


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


@admin.register(profile)
class ProfileCreateAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    date_hierarchy = 'date'
    search_fields = ('username__username', 'mobile_number')
    list_filter = ['operator', ("date", DateRangeFilter)]
    list_display = ['username', 'mobile_number', 'operator']


@admin.register(activation_data)
class ActivationDetailsAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    date_hierarchy = 'date'
    search_fields = ['username', 'code', 'mobile_number']
    list_filter = ['status', ("date", DateRangeFilter)]
    list_display = ['username', 'mobile_number', 'code', 'token', 'status', 'date']
