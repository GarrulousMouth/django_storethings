# Получение избранных товаров пользователя
# Контекст создан для того, чтобы на любой странице пользователь
# при добавление продукта в избранное, продукт проверялся на его наличие у пользователя
def favourite(request):
    try:
        user = request.user
        favourites = user.favourites.all()
        return {'favourite': favourites}
    except AttributeError:
        return []