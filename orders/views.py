from django.shortcuts import redirect  
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.views.generic import FormView , DetailView, UpdateView, ListView
from django.urls import reverse_lazy  
from django.contrib import messages  
from cart.utils import get_or_create_cart    # cartni olish uchun (sizda bor)
from .forms import CheckoutForm  , OrderStatusForm
from django.db import transaction  
from .models import OrderItem  , Order
from catalog.mixins import SellerRequiredMixin
class CheckoutView(LoginRequiredMixin, FormView):
   template_name = "orders/checkout.html"  # checkout template
   form_class = CheckoutForm  # form
   success_url = reverse_lazy("my_orders")  # order bo‘lgach historyga qaytamiz
   def get_context_data(self, **kwargs):
       ctx = super().get_context_data(**kwargs)
       cart = get_or_create_cart(self.request.user)  # user cartini olamiz
       ctx["cart"] = cart  # template’da ko‘rsatish uchun
       ctx["items"] = cart.items.select_related("product")  # cart itemlar
       ctx["subtotal"] = cart.subtotal()  # cart subtotal
       ctx["delivery"] = cart.delivery()  # cart delivery
       ctx["total"] = cart.total()  # cart total
       return ctx

   @transaction.atomic  # hammasi bitta “paket” bo‘lib saqlansin
   def form_valid(self, form):
       cart = get_or_create_cart(self.request.user)  # cartni olamiz

       if cart.items.count() == 0:  # cart bo‘sh bo‘lsa order qilmaymiz
           messages.error(self.request, "Savatcha bo‘sh ❌")
           return redirect("cart_detail")

       order = form.save(commit=False)  # hozircha DB ga saqlamaymiz
       order.user = self.request.user  # order egasi — hozirgi user
       order.save()  # endi DB ga saqlaymiz (order id hosil bo‘ladi)

       # Cart itemlardan OrderItem yasaymiz + stock kamaytiramiz
       for item in cart.items.select_related("product"):
           product = item.product  # mahsulot obyekt

           if product.stock < item.qty:  # stock yetmasa
               messages.error(self.request, f"'{product.name}' uchun stock yetarli emas ❌")
               raise ValueError("Stock yetarli emas")  # atomic sabab hammasi bekor bo‘ladi

           OrderItem.objects.create(
               order=order,  # qaysi order
               product=product,  # qaysi product
               seller=product.seller,  # buyurtma qaysi sotuvchiga tegishli
               qty=item.qty,  # miqdor
               unit_price=item.unit_price,  # cartdagi narx
           )

           product.stock -= item.qty  # stock kamayadi
           product.save(update_fields=["stock"])  # faqat stockni saqlaymiz

       cart.items.all().delete()  # order bo‘lgach cartni bo‘shatamiz

       messages.success(self.request, f"Buyurtma yaratildi ✅ (Order #{order.id})")
       return redirect("order_detail", pk=order.pk)  # order detailga yuboramiz




class MyOrdersListView(LoginRequiredMixin, ListView):
   model = Order
   template_name = "orders/my_orders.html"
   context_object_name = "orders"
   paginate_by = 10  # 10 tadan ko‘rsatadi

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user).order_by("-created_at")  # faqat o‘z orderlari


class OrderDetailView(LoginRequiredMixin, DetailView):
   model = Order
   template_name = "orders/order_detail.html"
   context_object_name = "order"

   def get_queryset(self):
       return Order.objects.filter(user=self.request.user)  # boshqa user orderini ocholmaydi



class SellerOrderListView(SellerRequiredMixin, ListView):
   model = Order
   template_name = "orders/seller/order_list.html"
   context_object_name = "orders"
   paginate_by = 20  # sahifalab ko‘rsatish
   def get_queryset(self):
       # Seller hamma orderlarni ko‘radi (yangilari tepada)
       return Order.objects.select_related("user").order_by("-created_at")


class SellerOrderStatusUpdateView(SellerRequiredMixin, UpdateView):
   model = OrderItem  # status OrderItem’da turadi
   form_class = OrderStatusForm
   template_name = "orders/seller/order_status_update.html"
   success_url = reverse_lazy("seller_order_items")  # update’dan keyin listga qaytadi

   def get_queryset(self):
       # Seller faqat o‘z item’ining statusini o‘zgartira oladi (security!)
       return OrderItem.objects.filter(seller=self.request.user)

   def form_valid(self, form):
       # Status saqlanadi (UpdateView o‘zi save qiladi)
       resp = super().form_valid(form)
       messages.success(self.request, f"Order #{self.object.order_id} status yangilandi ✅")
       return resp


class SellerOrderItemListView(SellerRequiredMixin, ListView):
   model = OrderItem
   template_name = "orders/seller/order_items.html"
   context_object_name = "items"
   paginate_by = 20

   def get_queryset(self):
       # Seller faqat o‘ziga tegishli itemlarni ko‘radi
       return (
           OrderItem.objects
           .filter(seller=self.request.user)
           .select_related("order", "product", "order__user")  # buyer info uchun
           .order_by("-order__created_at")
       )
       
class SellerOrderItemDetailView(SellerRequiredMixin, DetailView):
   model = OrderItem
   template_name = "orders/seller/order_item_detail.html"
   context_object_name = "item"

   def get_queryset(self):
       # Seller faqat o‘z item’ini ocholadi (security!)
       return (
           OrderItem.objects
           .filter(seller=self.request.user)
           .select_related("order", "product", "order__user")
       )

