from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView
from shop.models import Product

# Create your views here.
class Favourites(TemplateView):
    template_name = 'favourites/favourites.html'

    def get(self, request):
        try:
            user = request.user
            favourite_products = user.favourites.all()
            context = {
                'favourite_products': favourite_products
            }

            return render(request, self.template_name, context)
        except AttributeError:
            return render(request, self.template_name, {'favourite_products': []})

class FavouritesAdd(CreateView):

    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, pk=product_id)
            if product.favourites.filter(id=request.user.id):
                product.favourites.remove(request.user)
            else:
                product.favourites.add(request.user)
            return redirect(request.META.get('HTTP_REFERER'))
        except TypeError:
            return redirect('signup')
