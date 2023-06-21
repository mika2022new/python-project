from django.forms import DateInput
from django_filters import FilterSet, DateFilter, MultipleChoiceFilter

from .models import Post, Category


class PostFilter(FilterSet):

    date = DateFilter(field_name='time_in',
    widget=DateInput(attrs={'type': 'date'}),
    label='Поиск по дате',
    lookup_expr='date__gte'
    )

    cat = MultipleChoiceFilter(field_name='category__category_name',
    choices=Category.CATEGORIES,
    label='Поиск по категории'
    )

    class Meta:

        model = Post
        
        fields = {
            'title': ['icontains'],
            'author__user': ['exact'],
       }