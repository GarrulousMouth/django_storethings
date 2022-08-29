from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, User
from .forms import SugnUpForm

# Регистрация
class SignUp(CreateView):
    form_class = SugnUpForm
    template_name = 'registration/singup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

# Вход
class Login(FormView):
    form_class = AuthenticationForm
    template_name = 'registration/login.html'
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
        return render(request, self.template_name, {'form': form})

# Выход
class Logout(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('home')