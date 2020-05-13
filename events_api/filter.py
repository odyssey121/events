import django_filters
from django_filters import rest_framework as filters
from events_api.models import Event


class EventFilter(filters.FilterSet):
    start = filters.IsoDateTimeFilter(field_name="event_date", lookup_expr='gte')
    end = filters.IsoDateTimeFilter(field_name="event_date", lookup_expr='lte')
    class Meta:
        model = Event
        fields = ['event_date']