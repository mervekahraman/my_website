from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render,redirect
from .models import Product, Category, Profile, OrderItem
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm,UpdateUserForm,UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart
from Payments.forms import ShippingAddressForm
from Payments.models import ShippingAddress, OrderItems,Order


def home(request):
    product = Product.objects.all()
    return render(request,'Shop_home.html',{'products':product})

# def update_usr(request):
#     if request.user.is_authenticated:
#         logged_user = User.objects.get(id= request.user.id)
#         shipping = ShippingAddress.get(user__id=request.user.id)
#         user_form = UpdateUserForm(request.POST or None, instance = logged_user)
#         shipping_form = ShippingAddressForm(request.POST or None,instance=shipping)
#         if user_form.is_valid():
#             user_form.save()
#
#             login(request,logged_user)
#             messages.success(request,"User Profile Updated")
#             return redirect('home')
#         return render(request,"update_usr.html",{"user_form":user_form,"shipping_form":shipping_form})
#     else:
#         messages.success(request,"You have to be logged in ")
#         return redirect("register")


def update_usr(request):
    if request.user.is_authenticated:
        logged_user = User.objects.get(id=request.user.id)
        shipping = ShippingAddress.objects.filter(user__id=request.user.id).first()

        user_form = UpdateUserForm(request.POST or None, instance=logged_user)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping)

        if request.method == 'POST':
            print("POST request received")

        if user_form.is_valid() and shipping_form.is_valid():
            print("Both forms are valid")

            user_instance = user_form.save()
            print("User form saved:", user_instance)

            shipping_instance = shipping_form.save(commit=True)
            shipping_instance.user = logged_user
            shipping_instance.save()
            print("Shipping form saved:", shipping_instance)

            login(request, logged_user)
            messages.success(request, "User Profile Updated")
            return redirect('home')

        else:
            print("Form errors:")
            print("User form errors:", user_form.errors)
            print("Shipping form errors:", shipping_form.errors)

        print("Rendering update_usr.html")
        return render(request, "update_usr.html", {"user_form": user_form, "shipping_form": shipping_form})

    else:
        messages.success(request, "You have to be logged in ")
        return redirect("home")

def about(request):
    return render(request,'About.html',{})


def login_us(request):
    if request.method == "POST":
        username = request.POST.get("Username")
        password = request.POST.get("Password")
        user_auth = authenticate(request, username=username, password=password)
        if user_auth is not None:
            login(request, user_auth)

            current_profile = Profile.objects.get(user=user_auth)

            cart_saved = current_profile.old_cart_values
            if cart_saved:
                convert_thecart = json.loads(cart_saved)
                cart = Cart(request)
                for key, value in convert_thecart.items():
                    cart.database_add(product=key, quantity=value)

            messages.success(request, "You are logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")
    else:
        return render(request, 'login.html', {})

def logout_us(request):
    logout(request)
    messages.success(request,("You are logged out."))
    return redirect('home')

def register_us(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, ("First part is done,please continue..."))
            return redirect("update_info")
        else:
            messages.success(request, ("There is an error present,try again"))
            return redirect("register")
    else:
        return render(request,'register.html', {"form": form})

def product_page(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,"product_page.html", {'product': product})

def categoryy(request, foo):
    foo = foo.replace('-', ' ')
    print("Category name from URL:", foo)
    try:
        category = Category.objects.get(name=foo)
        print("Category found:", category)
        prod = Product.objects.filter(category=category)
        return render(request, "category.html", {'products': prod, 'category': category})
    except ObjectDoesNotExist:
            print("Category not found")
            messages.error(request, "This category does not exist. Please choose another one.")
            return redirect('home')
def update_info(request):
    if request.user.is_authenticated:
        logged_user = Profile.objects.get(user__id= request.user.id)
        form = UserInfoForm(request.POST or None, instance = logged_user)
        if form.is_valid():
            form.save()

            messages.success(request,"Your Profile Info Updated")
            return redirect('home')
        return render(request,"update_info.html",{"form":form})
    else:
        messages.success(request,"You have to be logged in ")
        return redirect("home")

def search_bar(request):
    search_term = request.GET.get('search', '')
    items = Product.objects.all()

    if search_term:

        items = items.filter(
            Q(name__icontains=search_term) |
            Q(description_product__icontains=search_term)
        )
    else:
        messages.success(request, "No item present in that name")
    return render(request, "search_bar.html", {"items": items, "search_term": search_term})

# @login_required(login_url='accounts/login/')
# def orders(request):
#     user_profile = Profile.objects.get(user=request.user)
#     orders = OrderItem.objects.filter(customer=user_profile).order_by('-date')
#     return render(request, 'orders.html', {'orders': orders})
#

import logging

logger = logging.getLogger(__name__)


@login_required
def orders(request):
    if request.user.is_authenticated:
        user_profile = request.user.profile
        user_orders = OrderItem.objects.filter(customer=user_profile)
        return render(request, 'orders.html', {'orders': user_orders})
    else:
        return redirect('login')

    # if request.user.is_authenticated:
    #     try:
    #         profile = Profile.objects.get(user=request.user)
    #         user_orders = OrderItem.objects.filter(customer=profile).order_by('-date')
    #         return render(request, 'orders.html', {'orders': user_orders})
    #     except Profile.DoesNotExist:
    #         messages.error(request, "Profile does not exist for this user.")
    #         return redirect('home')
    # else:
    #     messages.success(request, "You have to be logged in")
    #     return redirect("home")

def place_order(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        cart = Cart(request)
        for item in cart:
            product = item['product']
            quantity = item['quantity']
            order_item = OrderItem.objects.create(
                product=product,
                customer=profile,
                quantity=quantity,
                address=profile.address,  # Assuming you want to use profile address
                phone=profile.phone  # Assuming you want to use profile phone
            )
            print(f"Order created: {order_item}")
        cart.clear()  # Clear the cart after placing order
        return redirect('orders')  # Redirect to orders page
    else:
        return redirect('login')


@login_required
def order_received(request):
    user_profile = Profile.objects.get(user=request.user)
    cart = request.session.get('cart', {})
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            product=product,
            customer=user_profile,
            quantity=quantity,
            address=user_profile.address,
            phone=user_profile.phone,
            status=True
        )
    # Clear the cart
    request.session['cart'] = {}
    return render(request, 'order_received.html')





