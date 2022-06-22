from logging import exception
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import *
from .forms import CheckOutForm
from django.contrib import messages

# Create your views here.


class BaseView(View):
    def __init__(self, **kwargs):
        self.views = {}
        self.views["categories"] = Category.objects.all()
        self.views["subcategories"] = SubCategory.objects.all()
        super(BaseView, self).__init__(**kwargs)


class Contactus(TemplateView):
    template_name = "contact.html"


class Shipping(TemplateView):
    template_name = "shipping.html"


class Checkout(CreateView):
    template_name = "checkout.html"
    form_class = CheckOutForm
    success_url = reverse_lazy('shipping')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["carts"] = Cart.objects.filter(
            username=self.request.user.username, checkout=False
        )
        return context

    def form_valid(self, form):

        set_data = form.save(commit=False)
        if Cart.objects.filter(
            username=self.request.user.username, checkout=False
        ).exists():
            cart = Cart.objects.get(username=self.request.user.username, checkout=False)
            get_item_name = Product.objects.get(name=cart.items.name)

            set_data.quantity = cart.quantity
            set_data.product = get_item_name
            set_data.price = cart.total
            set_data.save()
            messages.success(self.request,"your order has been placed sucessfully")
            try:
             Cart.objects.get(items=get_item_name,username=self.request.user.username,checkout=False).delete()
            except:
                raise Exception('data cannot be handel')
            
        else:
            raise TypeError("the data not found")
        
        

        return super(Checkout, self).form_valid(form)


class HomeView(BaseView):
    def get(self, request):
        self.views["new_products"] = Product.objects.filter(labels="new")
        self.views["hot_products"] = Product.objects.filter(labels="hot")
        self.views["offer_products"] = Product.objects.filter(labels="offer")
        self.views["sliders"] = Slider.objects.all()
        self.views["ads"] = Ad.objects.all()
        return render(request, "index.html", self.views)


class SubCategoryView(BaseView):
    def get(self, request, slug):
        subcat_id = SubCategory.objects.get(slug=slug).id
        self.views["subcat_products"] = Product.objects.filter(subcategory_id=subcat_id)
        return render(request, "subcategory.html", self.views)


class DetailView(BaseView):
    def get(self, request, slug):
        self.views["detail_products"] = Product.objects.filter(slug=slug)
        return render(request, "single.html", self.views)


from django.db.models import Q


class SearchView(BaseView):
    def get(self, request):
        query = request.GET["query"]
        if query == "":
            return redirect("/")
        else:
            lookups = Q(name__icontains=query) | Q(description__icontains=query)
            self.views["search_result"] = Product.objects.filter(lookups).distinct()
            self.views["search_for"] = query
            return render(request, "search.html", self.views)


from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        cpassword = request.POST["cpassword"]

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, "The username is already used.")
                return redirect("/signup")

            elif User.objects.filter(email=email).exists():
                messages.error(request, "The email is already used.")
                return redirect("/signup")

            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                user.save()
                return redirect("/")

        else:
            messages.error(request, "The password does not match")
            return redirect("/signup")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.error(request, "Username or password does not match.")
            return redirect("/login")

    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


def cal_cart(slug, username):
    price = Product.objects.get(slug=slug).price
    discounted_price = Product.objects.get(slug=slug).discounted_price
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        quantity = Cart.objects.get(
            username=username, slug=slug, checkout=False
        ).quantity
        quantity = quantity + 1
    else:
        quantity = 1

    if discounted_price > 0:
        original_price = discounted_price
        total = original_price * quantity
    else:
        original_price = price
        total = original_price * quantity

    return total, original_price, quantity


def cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        total, original_price, quantity = cal_cart(slug, username)
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(
            quantity=quantity, total=total
        )

    else:
        total, original_price, quantity = cal_cart(slug, username)
        data = Cart.objects.create(
            username=username,
            slug=slug,
            items=Product.objects.filter(slug=slug)[0],
            total=original_price,
        )
        data.save()
    return redirect("/mycart")


def delete_cart(request, slug):
    username = request.user.username
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        Cart.objects.filter(username=username, slug=slug, checkout=False).delete()
        return redirect("/mycart")


def remove_product(request, slug):
    username = request.user.username
    price = Product.objects.get(slug=slug).price
    discounted_price = Product.objects.get(slug=slug).discounted_price
    quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
    if quantity > 1:
        quantity = quantity - 1
        if discounted_price > 0:
            original_price = discounted_price
            total = original_price * quantity
        else:
            original_price = price
            total = original_price * quantity

        Cart.objects.filter(username=username, slug=slug, checkout=False).update(
            quantity=quantity, total=total
        )
        return redirect("/mycart")
    return redirect("mycart")


def add_wishlist(request, slug):
    username = request.user.username
    if Cart.objects.filter(username=username, slug=slug, checkout=False).exists():
        total, original_price, quantity = cal_cart(slug, username)
        Cart.objects.filter(username=username, slug=slug, checkout=False).update(
            quantity=quantity, total=total
        )

    else:
        total, original_price, quantity = cal_cart(slug, username)
        data = Cart.objects.create(
            username=username,
            slug=slug,
            items=Product.objects.filter(slug=slug)[0],
            total=original_price,
        )
        data.save()
    return redirect("wishlist")


def remove_wishlist(request, slug):
    username = request.user.username
    price = Product.objects.get(slug=slug).price
    discounted_price = Product.objects.get(slug=slug).discounted_price
    quantity = Cart.objects.get(username=username, slug=slug, checkout=False).quantity
    if quantity > 1:
        quantity = quantity - 1
        if discounted_price > 0:
            original_price = discounted_price
            total = original_price * quantity
        else:
            original_price = price
            total = original_price * quantity

        Cart.objects.filter(username=username, slug=slug, checkout=False).update(
            quantity=quantity, total=total
        )
        return redirect("wishlist")
    return redirect("wishlist")


class CartView(BaseView):
    def get(self, request):
        username = request.user.username
        self.views["cart_view"] = Cart.objects.filter(username=username, checkout=False)
        return render(request, "cart.html", self.views)


class WishlistView(BaseView):
    def get(self, request):
        username = request.user.username
        self.views["cart_view"] = Cart.objects.filter(username=username, checkout=False)
        return render(request, "wishlist.html", self.views)
