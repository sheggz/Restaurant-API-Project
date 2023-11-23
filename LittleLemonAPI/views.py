from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from .models import MenuItem, Cart, Order, OrderItem, Category
from .serializers import MenuItemSerializer, ManagerGroupSerializer, OrderItemSerializer, OrderSerializer, CartSerializer, DeliveryGroupSerializer, AddToCartSerializer
from .permissions import IsDelivery, IsManager
from django.contrib.auth.models import User, Group

# Create your views here.

# supports get and post (get for everyuser and post for manager only)
class MenuItemsView(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated, IsManager]
    lookup_field = "pk" # if it's a url that takes two path arguments, you can specify the fields using a list ["field a", "field b"]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    # authentication_classes =
    

    def get_permissions(self):  #this overrides what is set in the permission_classes attribute
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        else: 
           return [IsAuthenticated(), IsManager()] #you have to return a iterable of instantiated permission classes
    
#class DeliveryGroupManagementView(generics.ListCreateAPIView, generics.DestroyAPIView):   this throws an error and idk why
class DeliveryGroupManagementView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = DeliveryGroupSerializer
    queryset = Group.objects.get(name ="Delivery crew").user_set
    lookup_field = 'id'

    # overwrite create because we dont want to create a new object but add a user to the group
    def create(self, request):
        deliverygroup = Group.objects.get(name="Delivery crew")
        deliverygroup.user_set.add(User.objects.get(id = request.data.get("id")))
        return Response({"message":"added successfully"})
        pass
    
    # destroy maps to a detail link (a link with url parameter) 
    # we over write because we dont want to delete the user we just want to remove the user from the group
    def destroy(self, request, id):
        deliverygroup = Group.objects.get(name="Delivery crew")
        deliverygroup.user_set.remove(User.objects.get(id = request.data.get("id")))
        return Response({"message":"removed successfully"})


class ManagerGroupManagementView(viewsets.ModelViewSet):
    queryset = Group.objects.get(name="Manager").user_set.all()
    serializer_class = ManagerGroupSerializer
    lookup_field = ("id")

    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update"]:
            return []
        else:
             return [IsAuthenticated(), IsManager()]

    def create(self, request):
        print(request.data["id"])
    #    user = self.queryset.get(id=request.data["id"])     # what we want to add wont be in the queryset so we cant use this
        user = User.objects.get(id=request.data["id"])
        manager_group = Group.objects.get(name="Manager")
        if request.method == "POST": # not needed sha
            manager_group.user_set.add(user)
            return Response({"message": "updated"})

    def destroy(self, request, id):
        user = self.queryset.get(id=id)
        manager_group = Group.objects.get(name="Manager")
        manager_group.user_set.remove(user) #user_set is a way to access reverse foreignkey relationships
        return Response({"message": "removed"})


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self, *args, **kwargs):
        cart = Cart.objects.filter(user = self.request.user)
        return cart

#    def get(self, request, *args, **kwargs):
#        cart = Cart.objects.filter(user = self.request.user)
#        return Response(CartSerializer(cart).data)

    def post(self, request):
        #serialized_cart = AddToCartSerializer(data=request.data)
        #serialized_cart.is_valid(raise_exception=True)
        serializer = CartSerializer(data=request.data)
        print(serializer.initial_data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        
        # at this point the serializer has retrieved the menuitem object from the queryset
        id = serializer.validated_data["menuitem"]
        quantity = serializer.validated_data["quantity"]
        
        #item = get_object_or_404(MenuItem, id = id)
        item = serializer.validated_data["menuitem"]
        unit_price = item.price
        price = unit_price * int(quantity)
        serializer.save(user=request.user, unit_price=unit_price, price=price)
        print(serializer.data)
        #try:
        #    Cart.objects.create(user=request.user, menuitem=item, quantity = quantity, unit_price = unit_price, price = price)
        #except Exception as e:
        #    return Response({"message": f"{e}"})
        return Response({"message": "Item added to cart successfully"})
    
    def destroy(self, request):
        self.get_queryset().delete() # batch deleting all items in the queryset
        return Response({"Message":"Cart emptied"})


class OrderView(viewsets.ModelViewSet):
    pass

#
#
#        cartitems = Cart.objects.filter(user = request.user)
#        total = 0
#        for item in cartitems:
#            total = total + item.price
#        order = Order.objects.create(user = request.user, status = False, date = date.today(), total = total)



#
#class CartView(viewsets.ModelViewSet):
#    '''
#    set user to current user
#    should be list of menu items
#    once an order is placed:
#        an order item is created
#        the items in the cart list is moved
#        those items now become individual entries in the OrderItem table 
#        with their respective quantity and identified by the unique order ID
#    '''
#    serializer_class = CartSerializer
#    queryset = Cart.objects.all()
#    model = Cart
#    permission_classes = [IsAuthenticated] # any authenticated person is a customer and all actions here have to do with a customer
#
#
#    def list (self, request):
#        items = Cart.objects.filter(user=self.request.user)
#        return  items #Response(CartSerializer(items, many=True).data) #remember to add the status
#    
#
#    def create(self, request): #add menuitems to cart
#        if request.data:
#            # check if a cart with that user already exists
#            print(Cart.objects.filter(user = request.user))
#            
#            if Cart.objects.filter(user = request.user).exists() is False: #this is how to test for empty queryset
#                #items = []
#                
#                serializer = CartSerializer(data=request.data)
#                serializer.is_valid(raise_exception=True)
#                print(request.data)
#                print(serializer.validated_data)
#                item_unit_price = MenuItem.objects.get(pk=request.data["menuitem"]).price
#                #serializer.save(user=request.user, unit_price=[item_unit_price], )
#
#                Cart.objects.create(
#                    user=request.user, menuitem=[serializer.validated_data["menuitem"]], quantity=[serializer.validated_data["quantity"]],
#                    unit_price=item_unit_price, price= [item_unit_price * serializer.validated_data["quantity"]]
#                )
#                return Response({"message": "Successfully added"})
#            
#            else:
#                return Response({"message": "hmmm"})
#                pass
#    

        
    

#
#class DeliveryGroupManagementView(viewsets.ModelViewSet):
#    queryset = Group.objects.get(name="Delivery crew").user_set.all()
#    serializer_class = ManagerGroupSerializer
#    lookup_field = ("id")
#
#    def get_permissions(self):
#        if self.action in ["retrieve", "update", "partial_update"]:
#            return []
#        else:
#             return [IsAuthenticated(), IsManager()]
#
#    def create(self, request):
#        print(request.data["id"])
#    #    user = self.queryset.get(id=request.data["id"])     # what we want to add wont be in the queryset so we cant use this
#        user = User.objects.get(id=request.data["id"])
#        manager_group = Group.objects.get(name="Manager")
#        if request.method == "POST": # not needed sha
#            manager_group.user_set.add(user)
#            return Response({"message": "updated"})
#
#    def destroy(self, request, id):
#        user = self.queryset.get(id=id)
#        manager_group = Group.objects.get(name="Manager")
#        manager_group.user_set.remove(user)
#        return Response({"message": "removed"})
