import django_filters
from .models import *


class ModuleFilter(django_filters.FilterSet):
    # answers = django_filters.CharFilter(method='get_course_mod')

    class Meta:
        model = Quiz
        fields = ['module__course']

