from django.shortcuts import render,redirect

from Shop.models import OrderItem
from cart.cart import Cart
from Payments.forms import ShippingAddressForm,PaymentForm
from .models import ShippingAddress, Order, OrderItems
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
def payments_success(request):
    return render(request, "payments_success.html", {})

def checkout(request):
    cart_1 = Cart(request)

    if request.user.is_authenticated:
        logged_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = ShippingAddressForm(request.POST or None, instance=logged_user)
    else:
        form = ShippingAddressForm(request.POST or None)

    cart_prod = cart_1.get_prods
    qty = cart_1.get_quantities
    totals = cart_1.totals()

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(
            customer=request.user,
            # Add other necessary fields for the order
        )
        for item in cart_1.get_items():
            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price,
                customer=request.user
            )

    return render(request, "checkout.html", {"cart_prod": cart_prod, "quantities": qty, "totals": totals, "form": form})



@login_required(login_url='accounts/login/')
def info_page(request):
    cart_1 = Cart(request)
    cart_prod = cart_1.get_prods
    qty = cart_1.get_quantities
    totals = cart_1.totals()

    if request.method == 'POST':
        s_form = ShippingAddressForm(request.POST, instance=ShippingAddress.objects.get(user=request.user))
        bill = PaymentForm(request.POST)

        if s_form.is_valid() and bill.is_valid():
            return redirect('order_received')
        else:
            return render(request, "info_page.html", {
                "cart_prod": cart_prod,
                "quantities": qty,
                "totals": totals,
                "s_form": s_form,
                "bill": bill
            })
    else:
        s_form = ShippingAddressForm(instance=ShippingAddress.objects.get(user=request.user))
        bill = PaymentForm()
        return render(request, "info_page.html", {
            "cart_prod": cart_prod,
            "quantities": qty,
            "totals": totals,
            "s_form": s_form,
            "bill": bill
        })




# @login_required(login_url='accounts/login/')
# def info_page(request):
#     if request.method == 'POST':
#         s_form = ShippingAddressForm(request.POST)
#         cart_1 = Cart(request)
#         cart_prod = cart_1.get_prods
#         qty = cart_1.get_quantities
#         totals = cart_1.totals()
#
#         if request.user.is_authenticated:
#             bill = PaymentForm()
#             return render(request, "info_page.html",
#                           {"cart_prod": cart_prod, "quantities": qty, "totals": totals, "s_form": request.POST,"bill":bill})
#         else:
#             bill = PaymentForm()
#             return render(request, "info_page.html",
#                           {"cart_prod": cart_prod, "quantities": qty, "totals": totals, "s_form": request.POST,"bill":bill})
#     else:
#         cart_1 = Cart(request)
#         cart_prod = cart_1.get_prods
#         qty = cart_1.get_quantities
#         totals = cart_1.totals()
#         return render(request, "info_page.html", {"cart_prod": cart_prod, "quantities": qty, "totals": totals})





import logging

logger = logging.getLogger(__name__)
@transaction.atomic()
def order_received(request):
    if not request.user.is_authenticated:
        return redirect('accounts/login/')

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        shipping_address = ShippingAddress.objects.get(user=request.user)

        if payment_form.is_valid():
            try:
                money = request.POST.get('money')

                if not money:
                    raise ValueError("The total amount (money) is missing")

                order = Order.objects.create(
                    customer=request.user,
                    name=shipping_address.name,
                    email=shipping_address.email,
                    shippingaddress=f"{shipping_address.address}, {shipping_address.district}, {shipping_address.province}, {shipping_address.zipcode}",
                    money=money
                )

                cart_1 = Cart(request)
                items = cart_1.get_items()
                if not items:
                    raise ValueError("The cart is empty")

                for item in items:
                    OrderItems.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['price'],
                        customer=request.user
                    )

                cart_1.clear()

                return render(request, 'order_received.html', {'order': order})
            except Exception as e:
                logger.error(f"Error processing order for user {request.user.id}: {e}")
                messages.error(request, f"Error processing order: {e}")
                return render(request, 'error.html', {'error_message': str(e)})
        else:
            logger.error(f"Payment form errors: {payment_form.errors.as_json()}")
            messages.error(request, "Payment information is incorrect")
            return redirect('info_page')
    else:
        return redirect('home')

