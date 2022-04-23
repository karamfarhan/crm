from django.db.models import fields
from django.db.models.deletion import PROTECT
from django.forms import ModelForm
from .models import Order, Product, Customer, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserupdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']



class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'



class ProfileUdateForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_pic']