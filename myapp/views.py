from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
import re  # Regular expression module
from .models import Profile, Product, Cart, CartItem, ProductDetail
from django.http import JsonResponse

# Create your views here.
def myapp(request):
    return render(request, "login_page.html")

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            messages.error(request, 'Both Username and password are required.')
            return redirect('login_page')

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)  # Log the user in
            return redirect('home_page')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password')  # Show error message
            return redirect('login_page')

    return render(request, "login_page.html")

def signup_page1(request):
    if request.method == 'POST':
        email = request.POST['email']

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return redirect('signup_page1')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('signup_page1')
        else:
            request.session['email'] = email
            return redirect('signup_page2')

    return render(request, "signup_page1.html")

def signup_page2(request):
    email = request.session.get('email', '')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return redirect('signup_page2')

        # Validate username criteria
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', username):
            messages.error(request, 'Username must be alphanumeric and 3-30 characters long.')
            return redirect('signup_page2')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken. Please choose a different username.')
            return redirect('signup_page2')

        # Validate password criteria
        errors = validate_password(password)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('signup_page2')

        request.session['username'] = username
        request.session['password'] = password
        return redirect('signup_page3')
    
    return render(request, 'signup_page2.html', {'message': email})

def validate_password(password):
    errors = []
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long.')
    if not re.search(r'[A-Z]', password):
        errors.append('Password must contain at least one uppercase letter.')
    if not re.search(r'[a-z]', password):
        errors.append('Password must contain at least one lowercase letter.')
    if not re.search(r'\d', password):
        errors.append('Password must contain at least one digit.')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append('Password must contain at least one special character.')
    return errors

def signup_page3(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        birthdate = request.POST['birthdate']
        email = request.session.get('email', '')
        password = request.session.get('password', '')
        username = request.session.get('username', '')
     
        
        if not email or not password or not username:
            messages.error(request, "Session expired. Please restart the signup process.")
            return redirect('signup_page1')

        # Generate a verification code
        verification_code = str(random.randint(100000, 999999))
        
        # Store the verification code and other details in the session
        request.session['verification_code'] = verification_code
        request.session['fullname'] = fullname
        request.session['birthdate'] = birthdate

        # Send the verification email
        send_mail(
            'Your Verification Code',
            f'Your verification code is {verification_code}.',
            'youremail.com', 
            [email],
            fail_silently=False,
        )
        
        return redirect('verification')
    return render(request, "signup_page3.html")

def verification(request):
    # Check if required session data is available
    if 'verification_code' not in request.session or not request.session.get('email', ''):
        messages.error(request, "Verification process not started or session expired.")
        return redirect('signup_page1')

    if request.method == 'POST':
        input_code = request.POST.get('input')
        verification_code = request.session.get('verification_code', '')

        if input_code == verification_code:
            # Retrieve session data
            email = request.session.get('email', '')
            password = request.session.get('password', '')
            username = request.session.get('username', '')
            fullname = request.session.get('fullname', '')
            birthdate = request.session.get('birthdate', '')

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Create a Profile instance and save fullname and birthdate
            Profile.objects.create(user=user, fullname=fullname, birthdate=birthdate)

            # Completely clear the session after user creation
            request.session.flush()

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login_page')
        else:
            messages.error(request, 'Invalid verification code. Please try again.')
            return redirect('verification')

    # Render the verification page with the email to be verified
    email = request.session.get('email', '')
    return render(request, "verification.html", {'email': email})

def resend_verification(request):
    # Retrieve the email from the session
    email = request.session.get('email', '')

    if email:
        # Generate a new verification code
        verification_code = str(random.randint(100000, 999999))

        # Update the session with the new verification code
        request.session['verification_code'] = verification_code

        # Resend the email
        send_mail(
            'Your New Verification Code',
            f'Your new verification code is {verification_code}.',
            'youremail@gmail.com',  # Replace with your email
            [email],
            fail_silently=False,
        )

        messages.info(request, 'A new verification code has been sent to your email.')
    else:
        messages.info(request, 'Session expired. Please sign up again.')
        return redirect('signup_page1')

    return redirect('verification')

@login_required
def home_page(request):
    brand = request.GET.get('brand', '')  
    gender = request.GET.get('gender', '')  
    min_price = request.GET.get('min_price', '')  
    max_price = request.GET.get('max_price', '')  

    products = Product.objects.all()  # Start with all products

    # Filter by brand if selected
    if brand:
        products = products.filter(brand__iexact=brand)
    
    # Filter by gender if selected
    if gender:
        if gender == 'Men':
            products = products.filter(gender__iexact='Men')
        elif gender == 'Women':
            products = products.filter(gender__iexact='Women')

    # Filter by price range if both min_price and max_price are provided
    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            products = products.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass  # Ignore invalid input for price filter

    return render(request, 'home_page.html', {'products': products})

# View for adding items to the cartcart
@login_required
def add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=400)

    # Get the requested quantity from GET parameters; default to 1
    try:
        qty = int(request.GET.get('qty', 1))
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1

    # Get or create the active cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)

    # Get or create the cart item for this product
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        # If the product is already in the cart, increase the quantity by the requested amount
        cart_item.quantity += qty
    else:
        # If this is a new cart item, set its quantity to the requested amount
        cart_item.quantity = qty
    cart_item.save()

    return JsonResponse({'success': True, 'message': 'Item added to cart' if created else 'Item quantity updated in cart'}, status=200)

# View for displaying the cart
@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user, active=True).first()
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
    else:
        cart_items = []
        total_price = 0

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# View for updating the cart quantity
@login_required
def update_cart_quantity(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)

    # Check if action is 'increase' or 'decrease'
    if 'increase' in request.GET:
        cart_item.quantity += 1
    elif 'decrease' in request.GET and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()
    return redirect('view_cart')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('view_cart')

@login_required
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login_page')

@login_required
def about(request):
    return render(request, "about.html")

@login_required
def contact(request):
    return render(request, "contact.html")

@login_required
def profile(request):
    return render(request, "profile.html", {'profile_data': request.user.profile})

@login_required
def checkout(request):
    # Retrieve the active cart for the current user
    cart = Cart.objects.filter(user=request.user, active=True).first()
    
    if cart:
        # Get all items in the cart
        order_items = CartItem.objects.filter(cart=cart)
        # Calculate the total price by summing (quantity * price) for each item
        total_price = sum(item.quantity * item.product.price for item in order_items)
    else:
        order_items = []
        total_price = 0

    # Render the checkout template with order_items and total_price context variables
    return render(request, 'checkout.html', {
        'order_items': order_items,
        'total_price': total_price
    })

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        detail = product.detail
    except ProductDetail.DoesNotExist:
        detail = None

    return render(request, 'product_detail.html', {
        'product': product,
        'detail': detail,
    })
