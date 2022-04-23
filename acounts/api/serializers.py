
from django.db.models import fields
from rest_framework import serializers
from acounts.models import Customer, Product , Order, User

class CustomerSerializers(serializers.ModelSerializer):

    username = serializers.SerializerMethodField('get_username_from_customer')

    class Meta:
        model = Customer
        fields = ['name','phone','email','adress','date_created','username']

    def get_username_from_customer(self, customer):
        return customer.user.username




class RegisterSerializers(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model  = User
        fields  = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = User(
            username = self.validated_data['username'],
            email    = self.validated_data['email']
        )
        password  = self.validated_data['password']
        password2 = self.validated_data['password2']


        if password != password2:
            raise serializers.ValidationError({'password':'password must be mutch'})

        user.set_password(password)
        user.save()
        return user



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username','email']
        



















class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'