from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters

User = get_user_model()


class UserSetFilter(FilterSet):
    distance = filters.RangeFilter(field_name='distance', method='filter')
    sex = filters.CharFilter(lookup_expr='exact')
    first_name = filters.CharFilter(lookup_expr='exact')
    last_name = filters.CharFilter(lookup_expr='exact')

    def filter(self, queryset, name, value):
        if name != 'distance':
            return queryset
        latitude = float(self.request.user.latitude)
        longitude = float(self.request.user.longitude)
        min_distance = value.start
        max_distance = value.stop
        milestokiolmetrs = 0.621371

        if min_distance:
            queryset = queryset.extra(
                where=[f'SQRT(POW(69.1 * ({latitude} - latitude), 2)'
                       f' + POW(69.1 * (longitude - {longitude})'
                       f' * COS({latitude} / 57.3), 2)) >= %s::float'],
                params=[float(min_distance) * milestokiolmetrs]
            )

        if max_distance:
            queryset = queryset.extra(
                where=[f'SQRT(POW(69.1 * ({latitude} - latitude), 2) '
                       f'+ POW(69.1 * (longitude - {longitude})'
                       f' * COS({latitude} / 57.3), 2)) <= %s::float'],
                params=[float(max_distance) * milestokiolmetrs]
            )

        return queryset.filter()

    class Meta:
        model = User
        fields = ['distance', 'first_name', 'last_name', 'sex']
