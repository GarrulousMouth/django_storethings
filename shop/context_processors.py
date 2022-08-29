from .models import Category

# Меню категорий, которые сущестуют
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)