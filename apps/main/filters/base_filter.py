from django_filters.rest_framework import FilterSet, DateFilter


class BaseFilter(FilterSet):
    begin_date = DateFilter(field_name='created_date', lookup_expr='date__gte')
    end_date = DateFilter(field_name='created_date', lookup_expr='date__lte')
