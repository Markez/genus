# Register your models here.
import csv

from django.contrib import admin
from django.db.models import Count, Sum, DateTimeField, Min, Max
from django.db.models.functions import Trunc
from django.http import HttpResponse
from rangefilter.filter import DateRangeFilter

from .models import africasTalkingResponses, AfrikaStalkingSMSMetrics


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


@admin.register(africasTalkingResponses)
class AfricastalkingSentSMSAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]
    date_hierarchy = 'date'
    search_fields = ('sms_target', 'username', 'mobile_number')
    list_filter = ['status', 'sms_target', ("date", DateRangeFilter)]
    list_display = ['username', 'mobile_number', 'sms_target', 'response_message', 'status',
                    'statusCode', 'cost', 'number', 'messageId', 'date']

class AfricaStalkingMetricsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    search_fields = ('sms_target', )
    list_filter = ('sms_target', 'date',)
    change_list_template = 'admin/africa_stalking_cost_summary.html'
    date_hierarchy = 'date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context, )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        metrics = {
            'total': Count('sms_target'),
            'total_sent': Sum('total_sent'),
            'total_cost': Sum('total_cost')
        }
        response.context_data['summary'] = list(
            qs
                .values('sms_target')
                .annotate(**metrics)
                .order_by('-date')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        #graphical display
        def get_next_in_date_hierarchy(request, date_hierarchy):
            if date_hierarchy + '__day' in request.GET:
                return 'hour'
            if date_hierarchy + '__month' in request.GET:
                return 'day'
            if date_hierarchy + '__year' in request.GET:
                return 'week'
            return 'month'
        period = get_next_in_date_hierarchy(
            request, self.date_hierarchy,
        )
        response.context_data['period'] = period
        summary_over_time = qs.annotate(
            period=Trunc('date', 'period', output_field=DateTimeField(),), )\
            .values('date').annotate(total=Sum('total_cost')).order_by('date')
        summary_range = summary_over_time.aggregate(
            low=Min('total'),
            high=Max('total'),
        )
        high = summary_range.get('high', 0)
        low = summary_range.get('low', 0)
        response.context_data['summary_over_time'] = [{
            'period': x['date'],
            'total': x['total'] or 0,
            'pct': ((x['total'] or 0) - low) / (high-low) * 100
            if high > low else 0,
        } for x in summary_over_time]

        return response

admin.site.register(AfrikaStalkingSMSMetrics,AfricaStalkingMetricsAdmin)
