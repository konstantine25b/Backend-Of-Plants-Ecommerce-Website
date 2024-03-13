from rest_framework import serializers
from .models import *
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        
        extra_kwargs = {
            'password': {'write_only' :True}
        }
        
    def create(self, validated_data):
        user = CustomUser(
            email= validated_data['email'],
            username = validated_data['username'],
            role = validated_data['role'],
            is_superuser= validated_data['is_superuser'],
            is_staff = validated_data['is_staff']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user

   

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        
        extra_kwargs = {
            'password': {'write_only' :True}
        }
        
    def create(self, validated_data):
        user = CustomUser(
            email= validated_data['email'],
            username = validated_data['username'],
            role = validated_data['role'],
            is_superuser= validated_data['is_superuser'],
            is_staff = validated_data['is_staff']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']
        
        extra_kwargs = {
            'password': {'write_only' :True}
        }
        
    def create(self, validated_data):
        user = CustomUser(
            email= validated_data['email'],
            username = validated_data['username'],
            role = validated_data['role'],
            is_superuser= validated_data['is_superuser'],
            is_staff = validated_data['is_staff']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        return user

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

