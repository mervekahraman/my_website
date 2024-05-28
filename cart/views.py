from django.shortcuts import render,get_object_or_404
from .cart import Cart
from Shop.models import Product
from django.http import JsonResponse
def cart_sum(request):
    cart_1 = Cart(request)
    cart_prod = cart_1.get_prods
    qty = cart_1.get_quantities
    totals = cart_1.totals()
    return render(request,"cart_summary.html",{"cart_prod":cart_prod,"quantities":qty,"totals":totals})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        product_qty = int(request.POST.get("product_qty"))
        product = get_object_or_404(Product,id=product_id)
        cart.add(product=product,quantity = product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response

# def cart_add(request):
#     cart = Cart(request)
#
#     if request.method == 'POST':
#         product_id = request.POST.get("product_id")
#         quantity = int(request.POST.get("quantity", 1))  # Default quantity is 1
#
#         # Retrieve the product object
#         product = get_object_or_404(Product, id=product_id)
#
#         # Add the product to the cart
#         cart.add(product=product, quantity=quantity)
#
#         # Return JSON response with updated cart quantity
#         cart_quantity = cart.__len__()
#         return JsonResponse({'qty': cart_quantity})
#
#     # Handle cases where method is not POST
#     return JsonResponse({'error': 'Invalid request method'})

def cart_del(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        cart.delete(product=product_id)
        cart_quantity = cart.__len__()
        # product_qty = int(request.POST.get('product_qty'))
        # cart.update(product = product_id,quantity=product_qty)
        #response = JsonResponse({'qty':product_qty})
        response = JsonResponse({'qty': cart_quantity})
        return response

def cart_upt(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity"))
        product = get_object_or_404(Product,id= product_id)
        cart.update(product = product,quantity = quantity)
        response = JsonResponse({'quantity':quantity})
        return response





