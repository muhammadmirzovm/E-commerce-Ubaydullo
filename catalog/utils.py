from orders.models import  OrderItem


def can_review(user, product):
   # 1) login bo'lishi shart (guest bo'lsa False)
   if not user.is_authenticated:
       return False

   # 2) user shu productni buyurtma qilganmi + delivered bo'lganmi?
   return OrderItem.objects.filter(
       order__user=user,          # shu userniki bo'lsin
       product=product,           # shu product bo'lsin
       status="delivered"  # order delivered bo'lsin (qabul qilingan)
   ).exists()
