from email.headerregistry import Group
from unicodedata import category
from rest_framework import serializers
from .models import MenuItem, Category, Order, OrderItem, Cart
from django.contrib.auth.models import Group, User
# import logging

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "slug", "title"]
        model = Category

        extra_kwargs = {
            "slug":{"read_only": True},

        }
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class ManagerGroupSerializer(serializers.ModelSerializer):
    #user = UserSerializer(read_only=True, many=True)
    #user_set__username = serializers.CharField(max_length=255)

#    def create(self, instance, validated_data):
#        user = instance.get(username=validated_data["id"])
#        manager_group = Group.objects.get(name="Manager")
#        if self.context["request"].method == "POST":
#            manager_group.user_set.add(user)
#            return Response({"message": "updated"})
#        if self.context["request"].method == "DELETE":
#            manager_group.user_set.remove(user)
#            return Response({"message": "removed"})
#        return Response({"message": "error"})

    class Meta:
        model = User
        fields = ["id", "username", "first_name","last_name", "groups"]
        read_only = ["username", "first_name", "last_name", "groups"]
        # "user_set__first_name", "user_set__last_name"]
        extra_kwargs = {
        #    "groups": {"many":"True"}

        }


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # required is true by default though, just felt like
    category_id = serializers.IntegerField(write_only=1)  
    #print( MenuItemSerializer.initial_data)
    class Meta:
        model = MenuItem
        fields = ['id', "title", "price", "featured", "category", "category_id"]

class DeliveryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name","last_name", "groups"]
        read_only = ["username", "first_name", "last_name", "groups"]

        

class OrderSerializer(serializers.ModelSerializer):
    pass
    #    model = Category
    #    fields = []
    #class Meta:


class OrderItemSerializer(serializers.ModelSerializer):
    pass


class CartMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price"]

class CartSerializer(serializers.ModelSerializer):
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all()) #the aregument is used in the desrialization process
    #price = serializers.SerializerMethodField(method_name="calculated_price") 
    
#   user = serializers.PrimaryKeyRelatedField(write_only=True, )
#   menuitem = CartMenuSerializer()
    class Meta:
        model = Cart
        fields = ["menuitem", "quantity", "price"]
        read_only_fields=["price"]
        
    #def calculated_price (self, obj:cart):
    #    return obj.unit_price * obj.quantity 

class AddToCartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = ["menuitem", "quantity"]



#class CartSerializer(serializers.ModelSerializer):
#    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all(), many=True)
#    price = serializers.SerializerMethodField(method_name="calculated_price")
#    class Meta:
#        model = Cart
#        fields = ["user", "menuitem", "quantity", "unit_price", "price" ]
#        
#        # we dont need to supply thesse when deserializing
#        extra_kwargs = {
#            "user": {"read_only": "True"},
#            "unit_price":{"read_only": "True"},
#            "price":{"read_only": "True"},
#        }
#    
#    def calculated_price (self, obj:Cart):
#        return obj.unit_price * obj.quantity 



