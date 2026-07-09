from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
   class Meta:
       model = Product
       fields = (
           "category","name","slug","price","short_description",
           "description","stock","is_active","main_image",)



class ReviewForm(forms.ModelForm):
   class Meta:
       model = Review
       fields = ("rating", "comment")

   rating = forms.ChoiceField(  # dropdown qilib beramiz (boshlang'ichlar uchun oson)
       choices=[(i, f"{i*"⭐"}") for i in range(1, 6)],
       widget=forms.Select(attrs={"class": "form-select"})
   )
   comment = forms.CharField(
       required=False,
       widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Izoh... (ixtiyoriy)"})
   )
