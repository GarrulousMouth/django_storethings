from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, FormView, DetailView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, User
from .forms import SugnUpForm
from .models import Category, Product as ProductModel

class HomeView(ListView):
    template_name = 'shop/home.html'
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get('search-product')
        if query is not None:
            return ProductModel.objects.filter(name__icontains=query)
        try:
            category_slug = self.kwargs['category_slug']
            category_page = get_object_or_404(Category, slug=category_slug)
            return ProductModel.objects.filter(category=category_page, available=True)
        except KeyError:
            return ProductModel.objects.all()


class Product(DetailView):
    def get(self, request, category_slug, product_slug):
        try:
            product = ProductModel.objects.get(category__slug=category_slug, slug=product_slug)
        except Exception as e:
            raise e
        return render(request, 'shop/product.html', {'product': product})

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

class Logout(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('home')
