from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name','role', 'last_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        # Check if the password is being updated
        if 'password' in validated_data:
            # Hash the password
            validated_data['password'] = make_password(validated_data['password'])
        # Update the instance with the validated data
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name','role', 'last_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    def update(self, instance, validated_data):
        # Check if the password is being updated
        if 'password' in validated_data:
            # Hash the password
            validated_data['password'] = make_password(validated_data['password'])
        # Update the instance with the validated data
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        # Check if the password is being updated
        if 'password' in validated_data:
            # Hash the password
            validated_data['password'] = make_password(validated_data['password'])
        # Update the instance with the validated data
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
       
