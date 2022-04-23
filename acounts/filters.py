from django.db.models import fields
import django_filters
from .models import *
from django import forms
from django_filters import DateFilter


#class totalorderfilter(django_filters.FilterSet):
 #   start_date = DateFilter(field_name="date_created", lookup_expr='gte')
  #  end_date = DateFilter(field_name="date_created", lookup_expr='lte')
   # class Meta:
    #    model = Order
     #   fields = ['customer','product','start_date','end_date']



class customerfilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['name']



#class productfilter(django_filters.FilterSet):
#    class Meta:
 #       model = Product
  #      fields = ['name']