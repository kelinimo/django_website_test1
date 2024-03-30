from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from user.forms import UserForm, CustomUserCreationForm

# Create your views here.


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/user_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_form'] = PasswordChangeForm(user=self.request.user)
        context['user_form'] = UserForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
        if password_form.is_valid():
            password_form.save()
        return self.render_to_response(self.get_context_data())



def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("store:index"))
        return render(request, "registration/register.html", {"form": form})
