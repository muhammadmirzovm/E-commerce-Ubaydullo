from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView,UpdateView
from .models import User
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy("product_list")
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Ro'yxatdan o'tish muvaffaqiyatli.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Ro'yxatdan o'tishda xatolik bor.")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
   template_name = "accounts/login.html"

   def form_valid(self, form):
       messages.success(self.request, "Tizimga kirdingiz ✅")
       return super().form_valid(form)

   def form_invalid(self, form):
       messages.error(self.request, "Login yoki parol xato ❌")
       return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = "product_list"

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Tizimdan chiqdingiz .")
        return super().dispatch(request, *args, **kwargs)
    

class ProfileDetailView( DetailView):
    model = User
    template_name = "accounts/profile_detail.html"
    context_object_name = "profile_user"
    
    def get_object(self):
        return self.request.user
    
    
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "accounts/profile_edit.html"
    form_class =  ProfileForm
    success_url = reverse_lazy("profile_detail")
    def get_object(self):
        return self.request.user
    def form_valid(self, form):
        messages.success(self.request, "Profil yangilandi")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Yangilashda xatolik !")
        return super().form_invalid(form)
    
    