from rest_framework import permissions
from rest_framework import response
from django.contrib.auth.models import User, Group

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        print(".groups.all()", request.user.groups.all())
        print(".groups", request.user.groups)
        print(".groups.values", request.user.groups.values())
        print(".groups.filter()", request.user.groups.filter)
        return request.user.groups.filter(name = "Manager").exists()

class IsDelivery(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user.groups.all().filter(name = "Delivery crew").exists() #it is user.groups not user.group


