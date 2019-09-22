from main.filters import BaseFilter
from django_filters import DateFilter, CharFilter, ChoiceFilter
from main.helpers import is_int


class MembershipFilterSet(BaseFilter):
    EMPLOYEE = 'employee'
    MANAGER = 'manager'
    OWNER = 'owner'
    POSITION_TYPES = (
        (EMPLOYEE, 'employee'),
        (MANAGER, 'manager'),
        (OWNER, 'owner'),
    )
    date_joined_begin = DateFilter(field_name='date_joined', lookup_expr='gte')
    date_joined_end = DateFilter(field_name='date_joined', lookup_expr='lte')
    role = ChoiceFilter(choices=POSITION_TYPES)
    stock = CharFilter(method='get_stocks')
    member = CharFilter(method='get_members')

    def get_stocks(self, query, name, value: str):
        value_list = value.split('-')
        if all(is_int(val) for val in value_list):
            return query.filter(stock__id__in=value_list)
        return query

    def get_members(self, query, name, value: str):
        value_list = value.split('-')
        if all(is_int(val) for val in value_list):
            return query.filter(member__id__in=value_list)
        return query
