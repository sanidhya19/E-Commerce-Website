from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import stripe
from django.conf import settings
from .models import Product, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, ShippingAddressForm, ContactForm
from .cart import Cart
from django.views import View
from .models import CartItem, ShippingAddress
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
#Test#123

def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})

def about(request):
	return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            login(request, user)
            request.session["user_info"] = {
                "username" : user.username,
                "email" : user.email,
            }
            messages.success(request, "You have logged in successfully!")
            return redirect('home')
        else:
          
            messages.error(request, 'Invalid username or password. Please try again.')
            return render(request, 'login.html')
    return render(request, 'login.html')
	


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out."))
	return redirect('home')



def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')  
            return redirect('home')
        else:      
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})



@login_required(login_url='login')  
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    product = Product.objects.get(id=product_id)

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
    else:
        cart[str(product_id)] = {
            "name": product.name,
            "price": int(product.price),
            "quantity": 1
        }

    request.session["cart"] = cart  
    request.session.modified = True
    return redirect("cart")

def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart.html', {
        'cart_items': cart.get_items(),
        'total_price': cart.get_total_price(),
    })

def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart')

def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']  
    return redirect('cart')


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def add_address(request):
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            request.session["shipping_address"] = {
                "address": address.address,
                "city": address.city,
                "state": address.state,
                "postal_code": address.postal_code,
                "country": address.country,
            }
            return redirect("checkout")
    else:
        form = ShippingAddressForm()
    
    return render(request, "add_address.html", {"form": form})


@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect("cart")

    # Calculate total price
    total_price = sum(item["price"] * item["quantity"] for item in cart.values())
    
    if total_price <= 0:
        messages.error(request, "Invalid cart total!")
        return redirect("cart")

    if request.method == "POST":
        address_id = request.POST.get("address_id")  # Match name from form
        new_address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country")

        if address_id and address_id != "new":  
            # User selected a saved address
            try:
                shipping_address = ShippingAddress.objects.get(id=address_id, user=request.user)
            except ShippingAddress.DoesNotExist:
                messages.error(request, "Invalid address selection.")
                return redirect("checkout")
        elif new_address and city and state and postal_code and country:
            # User entered a new address
            shipping_address = ShippingAddress.objects.create(
                user=request.user,
                address=new_address,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
            )
        else:
            messages.error(request, "Please enter a valid shipping address!")
            return redirect("checkout")

        # Store selected shipping address in session
        request.session["shipping_address"] = shipping_address.id

        try:
            # Create Stripe checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Cart Items',
                            },
                            'unit_amount': int(total_price * 100),  # Convert dollars to cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/'),
            )

            return redirect(session.url, code=303)

        except Exception as e:
            print(f"Stripe Error: {e}")
            messages.error(request, "Payment could not be processed!")
            return redirect("checkout")

    saved_addresses = ShippingAddress.objects.filter(user=request.user)

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart.values(),
            "total_price": total_price,
            "saved_addresses": saved_addresses,
        },
    )

def payment_cancel(request):
    return redirect("cart")

@login_required
def payment_success(request):
    user = request.user
    shipping_address_id = request.session.get("shipping_address")

    # Fetch full address from the database
    shipping_address = None
    if shipping_address_id:
        shipping_address = ShippingAddress.objects.filter(id=shipping_address_id).first()

    if 'cart' in request.session:
        cart = request.session['cart']
        
        for product_id, item in cart.items():
            Order.objects.create(
                user_email=user.email,
                user=user,
                product_name=item['name'],
                product_price=item['price'],
                quantity=item['quantity'],
                total_cost=item['price'] * item['quantity'],
                shipping_address=(
                    f"{shipping_address.address}, {shipping_address.city}, {shipping_address.state}, "
                    f"{shipping_address.postal_code}, {shipping_address.country}" if shipping_address else "No Address Provided"
                ),
            )

        # Clear the cart after order is placed
        del request.session['cart']
        del request.session['shipping_address']  # Clear shipping address from session
        request.session.modified = True  

    return render(request, 'success.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = "whsec_z7cWZEVVv7ecsLGqwiBuAtE4X8PBtvk4"
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({"error": "Invalid payload"}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({"error": "Invalid signature"}, status=400)

    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        request.session["cart"] = {}  

    return JsonResponse({"status": "success"}, status=200)

    
def order_history(request):
    user_email = request.user.email 
    orders = Order.objects.filter(user__email=user_email)  

    return render(request, "order_history.html", {"orders": orders})


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your query has been submitted!")
            return redirect("contact_us")
    else:
        form = ContactForm()

    return render(request, "contact_us.html", {"form": form, "phone": "+1234567890", "email": "support@example.com"})
   




