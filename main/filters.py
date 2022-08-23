from django_filters import rest_framework as filters
from main.models import Favor, Subcategory


class FavorFilter(filters.FilterSet):
    class Meta:
        model = Favor
        fields = ('subcategory',)


class SubcategoryFilter(filters.FilterSet):
    class Meta:
        model = Subcategory
        fields = ('category',)
