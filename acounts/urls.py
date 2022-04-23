from django.urls import path
from django.urls.conf import include
from . import views
from django.contrib.auth import views as auth_views

#app_name = 'acounts'

urlpatterns = [
    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/', views.loginuser, name='login'),
    path('logout/', views.logoutuser, name='logout'),


    path('user_page/', views.userpage, name='user_page'),

    path('products/',views.products, name='products'),
    path('create_product/',views.createproduct, name='create_product'),
    path('update_product/<str:id>/',views.updateproduct, name='update_product'),
    path('delete_product/<str:id>/',views.deleteproduct, name='delete_product'),
    
    path('customer/<str:id>/',views.customer, name='customer'),
    path('customers_page/',views.customerspage, name='customers_page'),
    path('create_customer/',views.createcustomer, name='create_customer'),
    path('update_customer/<str:id>/',views.updatecustomer, name='update_customer'),
    path('delete_customer/<str:id>/',views.deletecustomer, name='delete_customer'),
    
    path('create_order/<str:id>/',views.createorder, name='create_order'),
    path('update_order/<str:id>/',views.updateorder, name='update_order'),
    path('delete_order/<str:id>/',views.deleteorder, name='delete_order'),
    path('total_order/',views.totalorder, name='totalorder'),
    
    

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="acounts/password_reset.html"),name="reset_password"),

    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name="acounts/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="acounts/password_reset_form.html"), name="password_reset_confirm"),

    path('passowrd_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="acounts/password_reset_complete.html"), name="password_reset_complete"),

]


# reset password steps
'''
1 - Submit email form                         //PasswordResetView.as_view() 
2 - Email sent success message                //PasswordResetDoneView.as_view() 
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view() 
'''