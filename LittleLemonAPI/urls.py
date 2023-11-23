from django.urls import path
from . import views

urlpatterns = [
   # path("/users",),
   # path("/users/me",),
    path("menu-items", views.MenuItemsView.as_view(
        {
            'get': 'list', 
            'post': 'create',
        }
        )),

    # the value put after int: has to correspond with the name of the field to be searched
    path("menu-items/<int:pk>", views.MenuItemsView.as_view(
        {
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy', 
        })),
    
    path("groups/manager/users", views.ManagerGroupManagementView.as_view({
            'get': 'list', 
            'post': 'create',
        })),

    path("groups/manager/users/<int:id>", views.ManagerGroupManagementView.as_view(
        {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy',}
    )),

    path("groups/delivery-crew/users", views.DeliveryGroupManagementView.as_view(
        {'get': 'list', 'post': 'create', }
    )),

    path("groups/delivery-crew/users/<int:id>", views.DeliveryGroupManagementView.as_view(
        { 'delete': 'destroy', }
    )),
   #path("cart/menu-items", views.CartView.as_view(
   #     {'get': 'get_qu', 'post': 'create', })),
    path("cart/menu-items", views.CartView.as_view()),
    
   # path("/orders",),
   # path("/orders/<int:orderId>",),
]