def favourite(request):
    try:
        user = request.user
        favourites = user.favourites.all()
        return {'favourite': favourites}
    except AttributeError:
        return []