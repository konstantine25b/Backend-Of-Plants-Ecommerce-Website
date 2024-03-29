from rest_framework import serializers
from .models import  Order, OrderItem

class OrderSerializer(serializers.ModelSerializer):
 

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at' , 'updated_at'] 
    
    

class OrderItemSerializer(serializers.ModelSerializer):
    
    
    # price = serializers.SerializerMethodField()
    # cost = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = '__all__'
        
        
    # def validate(self, validated_data):
    #     order_quantity = validated_data["quantity"]
    #     product_quantity = validated_data["product"].quantity
        
    #     if order_quantity > product_quantity:
    #         raise serializers.ValidationError("Ordered quantity is more than the stock.")
        
    # def get_price(self, obj):
    #     return obj.product.price

    # def get_cost(self, obj):
    #     return obj.cost