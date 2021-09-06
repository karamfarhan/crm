from django.urls import path
from acounts.api import views as api_views
from acounts.api.views import apicustomerlist,apilogin

#app_name = 'acounts'
urlpatterns = [
    path('', api_views.apiview, name='api'),
    path('customer/<str:pk>/', api_views.apicustomer, name='apicustomer'),
    path('customers/', apicustomerlist.as_view(), name='apicustomerlist'),
    path('update_customer/<str:pk>/', api_views.apicustomer_update, name='apicustomer_update'),
    path('delete_customer/<str:pk>/', api_views.apicustomer_delete, name='apicustomer_delete'),
    path('create_customer/', api_views.apicustomer_create, name='apicustomer_create'),

    path('register/', api_views.apiregister, name='apiregister'),
    path('user_detil/', api_views.apiuser_detil, name='apiuser_detil'),
    path('user_update/', api_views.apiuser_update, name='apiuser_update'),
    path('login/', apilogin.as_view(), name='apilogin'),

























    path('product/<str:pk>/', api_views.apipruduct, name='apiproduct'),
    path('order/<str:pk>/', api_views.apiorder, name='apiorder'),
    path('createorder/', api_views.apicreateorder, name='apicreateorder'),
    path('updateorder/<str:pk>/', api_views.apiupdateorder, name='apiupdateorder'),
    path('deleteorder/<str:pk>/', api_views.apideleteorder, name='apideleteorder'),



]