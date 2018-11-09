from django.contrib import admin
from .models import sentSMSLogs
from django.http import HttpResponse
from rangefilter.filter import DateRangeFilter

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


# Register your models here.
@admin.register(sentSMSLogs)
class sentSMSLogsAdmin(admin.ModelAdmin, ExportCsvMixin):
    action = ["export_as_csv"]
    date_hierarchy = 'date'
    search_fields = ('mobile_number',)
    list_filter = ('category', ("date", DateRangeFilter))
    list_display = ("username", "mobile_number", "message_sent", "category", "date")