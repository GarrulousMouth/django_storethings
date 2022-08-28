from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.models import User
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

class PersonalAccount(TemplateView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.user == user:
            return render(request, 'shop/personal_account.html', {'user': user})