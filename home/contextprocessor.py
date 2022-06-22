from .models import Cart


def cart(request):
    context={}
    if Cart.objects.filter(username=request.user.username, checkout=False).exists():
        context['cart']=Cart.objects.get(username=request.user.username, checkout=False)
    else:
        context['cart']=0

    return context