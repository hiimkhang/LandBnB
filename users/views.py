from django.views.generic import FormView, DetailView, UpdateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from . import models, forms, mixin
# Create your views here.

class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"

    pass

class UpdateProfileView(mixin.LoggedInOnlyView, SuccessMessageMixin, UpdateView): 
    model = models.User
    template_name = "users/update-profile.html" 
    fields = (     
        "first_name",
        "last_name",
        "gender",
        "avatar",
        "bio",
        "birthday",
        "language",
    )
    success_message = "Profile has been updated"

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self):
        form = super().get_form()
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["gender"].widget.attrs = {"placeholder": "Gender"}
        form.fields["bio"].widget.attrs = {"placeholder": "bio"}
        form.fields["birthday"].widget.attrs = {"placeholder": "Birthdate"}
        form.fields["language"].widget.attrs = {"placeholder": "Language"}
        return form

class UpdatePasswordView(mixin.LoggedInOnlyView, SuccessMessageMixin, PasswordChangeView):
    template_name = "users/update-password.html"
    success_message = "Password has been updated"

    def get_form(self):
        form = super().get_form()
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {"placeholder": "Confirm new password"}
        return form

    def get_success_url(self): 
        return self.request.user.get_absolute_url()

class LoginView(mixin.LoggedOutOnlyView, FormView):
    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            messages.info(self.request, f"Login succesfully")
            login(self.request, user)
        return super().form_valid(form)

class SignUpView(mixin.LoggedOutOnlyView, FormView): 
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home") 
    initial = {
        "first_name": "Khang",
        "last_name": "Phan",
        "email": "khang@test.com",
    }

    def form_valid(self, form): 
        form.save() 
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            messages.info(self.request, f"Register succesfully")
            login(self.request, user)
        return super().form_valid(form)

def log_out(request):
    logout(request)
    messages.info(request, f"See you later")
    return redirect(reverse("core:home"))

@login_required
def switch_hosting(request):
    try:
        del request.session["is_hosting"] 
    except KeyError:
        request.session["is_hosting"] = True 
    return redirect(reverse("core:home"))

def github_login(request):
    pass