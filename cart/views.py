from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product
from .models import CartItem
from .utils import get_or_create_cart
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Cart sahifasini ko‘rsatadigan view (faqat login bo‘lgan user kiradi)
class CartDetailView(LoginRequiredMixin, TemplateView):
   template_name = "cart/cart_detail.html"
   # Template'ga yuboriladigan ma'lumotlarni (context dictionary) tayyorlaymiz
   def get_context_data(self, **kwargs):
       # Django'ning default context'ini olib, ustiga o'zimizniki qo'shamiz
       ctx = super().get_context_data(**kwargs)  # context dictionary = template uchun data dict
       # Hozirgi user uchun cart'ni topamiz (yo'q bo'lsa yaratamiz)
       cart = get_or_create_cart(self.request.user)
       # Template'da ishlatish uchun cart obyektini yuboramiz
       ctx["cart"] = cart
       # Cart ichidagi itemlar (productlar bilan birga tezroq olish uchun select_related)
       ctx["items"] = cart.items.select_related("product")
       # Hisob-kitoblar: subtotal, delivery, total
       ctx["subtotal"] = cart.subtotal()
       ctx["delivery"] = cart.delivery()
       ctx["total"] = cart.total()
       # Tayyor context'ni template'ga qaytaramiz
       return ctx
# Cart'ga mahsulot qo'shish uchun view (faqat login bo'lgan user ishlata oladi)
class CartAddView(LoginRequiredMixin, View):
   # Bu view faqat POST so'rovda ishlaydi (form yuborilganda)
   def post(self, request, product_id):
       # 1) Hozirgi user uchun cart'ni topamiz (yo'q bo'lsa yaratamiz)
       cart = get_or_create_cart(request.user)
       # 2) Qo'shilayotgan product'ni bazadan topamiz (topilmasa 404)
       #    is_active=True -> faqat aktiv productlar qo'shilsin
       product = get_object_or_404(Product, id=product_id, is_active=True)
       # 3) Formadan kelgan qty ni olamiz (kelmasa default 1)
       #    POST dan kelgan qiymat string bo'ladi -> int ga aylantiramiz
       qty = int(request.POST.get("qty", 1))
       # 4) CartItem bor bo'lsa oladi, yo'q bo'lsa yaratadi
       #    defaults faqat yangi yaratilganda ishlaydi
       item, created = CartItem.objects.get_or_create(
           cart=cart,
           product=product,
           defaults={"qty": qty, "unit_price": product.price},
       )
       # 5) Agar bu product cart'da oldin ham bo'lgan bo'lsa (created=False)
       #    qty ni ustiga qo'shamiz va saqlaymiz
       if not created:
           item.qty += qty
           item.unit_price = product.price  # xohlasangiz birinchi narxda qoldirish ham mumkin
           item.save()
       # 6) Userga muvaffaqiyat xabarini chiqaramiz (messages framework)
       messages.success(request, "Savatchaga qo‘shildi ✅")
       # 7) Ish tugagach cart sahifasiga qaytaramiz
       return redirect("cart_detail")
class CartUpdateView(LoginRequiredMixin, View):
   def post(self, request, product_id):
       cart = get_or_create_cart(request.user)
       item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
       qty = int(request.POST.get("qty", 1))
       if qty < 0:
           item.qty += qty  
           item.save()
           messages.warning(request, "Item kamaytirildi 🗑️")
       elif qty == 0:
           messages.warning(request, "Item bir xil turibdi 🗑️")
       elif item.qty == 0:
           item.delete()
           messages.warning(request, "Item o'chirildi 🗑️")
       else:
           item.qty += qty
           item.save()
           messages.info(request, "Miqdor yangilandi ✅")
       return redirect("cart_detail") 
class CartRemoveView(LoginRequiredMixin, View):
   def post(self, request, product_id):
       cart = get_or_create_cart(request.user)
       item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
       item.delete()
       messages.warning(request, "Savatchadan o‘chirildi 🗑️")
       return redirect("cart_detail")

