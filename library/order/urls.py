
from django.urls import path
from . import views

urlpatterns = [
    path("orders/", views.order_list, name="order_list"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("orders/create/", views.create_order, name="create_order"),
    path(
        "orders/<int:order_id>/edit/",
        views.update_order,
        name="update_order",
    ),
    path(
        "orders/<int:order_id>/close/",
        views.close_order,
        name="close_order",
    ),
]
