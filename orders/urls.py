from django.urls import path
from . import views

urlpatterns = [
   path("checkout/", views.CheckoutView.as_view(), name="checkout"),  # checkout
   path("my-orders/", views.MyOrdersListView.as_view(), name="my_orders"),  # history
   path("my-orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),  # detail
]
