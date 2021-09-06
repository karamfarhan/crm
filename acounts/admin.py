from django.contrib import admin

from .models import *
# Register your models here.

admin.site.site_header = 'CRM Admin'
admin.site.site_title = 'CRM Admin Area'
admin.site.index_title = 'Welcome To The CRM Admin Area'



admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(Profile)