import django_filters

from Joo.models import Post


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = ['name', 'publication_date', 'publisher', 'description', 'num_visits', 'last_visit']
