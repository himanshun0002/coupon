from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .models import Coupon ,Realtor
from django.utils import timezone


# Create your views here.
def pre_home_screen(request):
    return render(request, "main_page/pre_home_screen.html")


from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Coupon


@login_required
def create_coupon(request):
    if request.method == "POST":
        code = get_random_string(8).upper()
        description = request.POST["description"]
        discount = request.POST["discount"]
        valid_from = request.POST["valid_from"]
        valid_to = request.POST["valid_to"]
        level = request.POST["level"]

        image = request.FILES.get("image")

        # Handle user roles
        if request.user.role == "user":
            # User must upload an image
            image = request.FILES.get("image")
            if not image:
                # Image is required for user
                return render(
                    request,
                    "main_page/create_coupon.html",
                    {"error": "Image is required for users."},
                )
        elif request.user.role == "manager":
            # Manager can optionally upload an image
            if request.POST.get("upload_image_checkbox"):
                image = request.FILES.get("image")

        coupon = Coupon.objects.create(
            code=code,
            description=description,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            owner=request.user,
            level=level,
            image=image,
        )
        return redirect("coupon_list")

    return render(request, "main_page/create_coupon.html")


# List Coupons
@login_required
def coupon_list(request):
    coupons = Coupon.objects.filter(is_active=True, valid_to__gte=timezone.now())
    return render(request, "main_page/coupon_list.html", {"coupons": coupons})


# Claim Coupon
@login_required
def claim_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.user.level != coupon.level:
        return render(
            request,
            "main_page/coupon_list.html",
            {"error": "You cannot claim this coupon!"},
        )

    coupon.is_active = False
    coupon.save()
    return redirect("generate_promo_code")


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    # ✅ Redirect if user is already authenticated
    if request.user.is_authenticated:
        return redirect("dashboard")  # or use your namespaced route

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("pre_home_screen")  # redirect to dashboard after login
        else:
            return render(
                request, "main_page/login.html", {"error": "Invalid credentials"}
            )

    return render(request, "main_page/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


from django.shortcuts import render, redirect
from .models import User  # Import the custom User model
from django.contrib.auth import login
from django.contrib.auth import get_user_model


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        role = request.POST["role"]
        level = request.POST["level"]

        User = get_user_model()
        # Check if username already exists

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "main_page/register.html",
                {
                    "error": "Username already exists",
                    "username": username,
                    "email": email,
                    "role": role,
                    "level": level,
                },
            )

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(
                request,
                "main_page/register.html",
                {
                    "error": "Email already exists",
                    "username": username,
                    "email": email,
                    "role": role,
                    "level": level,
                },
            )

        # Create the user
        user = User.objects.create_user(
            username=username, email=email, password=password, role=role, level=level
        )

        # Optionally, you can assign groups here if required
        # user.groups.add(group)

        # Redirect to login page after successful registration
        return redirect("login")

    return render(request, "main_page/register.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, ManagerProfile
from django.contrib import messages


@login_required
def user_profile_view(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_profile.full_name = request.POST.get("full_name", "")
        user_profile.address = request.POST.get("address", "")
        user_profile.gender = request.POST.get("gender", "")

        profile_photo = request.FILES.get("profile_photo")
        background_photo = request.FILES.get("background_photo")

        if profile_photo:
            user_profile.profile_photo = profile_photo
        if background_photo:
            user_profile.background_photo = background_photo

        user_profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("user_profile")

    return render(
        request, "main_page/user_profile.html", {"user_profile": user_profile}
    )


@login_required
def manager_profile_view(request):
    manager_profile, _ = ManagerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        manager_profile.full_name = request.POST.get("full_name", "")
        manager_profile.address = request.POST.get("address", "")
        manager_profile.gender = request.POST.get("gender", "")
        manager_profile.gst_number = request.POST.get("gst_number", "")
        manager_profile.shop_number = request.POST.get("shop_number", "")
        manager_profile.owner_aadhar_number = request.POST.get(
            "owner_aadhar_number", ""
        )

        # Handle file uploads safely
        manager_profile.profile_photo = request.FILES.get(
            "profile_photo", manager_profile.profile_photo
        )
        manager_profile.background_photo = request.FILES.get(
            "background_photo", manager_profile.background_photo
        )
        manager_profile.shop_photo = request.FILES.get(
            "shop_photo", manager_profile.shop_photo
        )
        manager_profile.owner_aadhar_photo = request.FILES.get(
            "owner_aadhar_photo", manager_profile.owner_aadhar_photo
        )
        manager_profile.selfie_with_shop = request.FILES.get(
            "selfie_with_shop", manager_profile.selfie_with_shop
        )

        manager_profile.save()
        messages.success(request, "Manager profile updated successfully!")
        return redirect("manager_profile")

    return render(
        request, "main_page/manager_profile.html", {"manager_profile": manager_profile}
    )


from django.shortcuts import render
from .models import UserProfile, ManagerProfile, Coupon


def dashboard(request):
    user = request.user
    user_profile = None
    manager_profile = None
    coupons = Coupon.objects.filter(owner=user)  # Get coupons created by this user

    if user.role == "user":
        user_profile = UserProfile.objects.filter(user=user).first()
    elif user.role == "manager":
        manager_profile = ManagerProfile.objects.filter(user=user).first()

    return render(
        request,
        "main_page/dashboard.html",
        {
            "user": user,
            "user_profile": user_profile,
            "manager_profile": manager_profile,
            "coupons": coupons,
            "coupon_count": coupons.count(),
        },
    )


import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import OTPVerification
from .utils import send_whatsapp_otp


# Step 1: Request OTP Before Login
def request_login_otp(request):
    if request.method == "POST":
        phone_number = request.POST["phone_number"]
        user_otp, created = OTPVerification.objects.get_or_create(
            phone_number=phone_number
        )

        # Generate and send OTP via WhatsApp
        user_otp.generate_otp()
        if send_whatsapp_otp(phone_number, user_otp.otp):
            request.session["phone_number"] = phone_number
            return redirect("verify_login_otp")  # Redirect to OTP verification page

    return render(request, "main_page/request_otp.html")


# Step 2: Verify OTP Before Login
def verify_login_otp(request):
    phone_number = request.session.get("phone_number")
    if not phone_number:
        return redirect("request_login_otp")

    try:
        user_otp = OTPVerification.objects.get(phone_number=phone_number)
    except OTPVerification.DoesNotExist:
        return redirect("request_login_otp")

    if request.method == "POST":
        entered_otp = request.POST["otp"]

        if entered_otp == user_otp.otp:
            user_otp.is_verified = True
            user_otp.save()
            return redirect(
                "register_view"
            )  # Redirect to login after successful OTP verification
        else:
            return render(
                request, "main_page/verify_otp.html", {"error": "Invalid OTP"}
            )

    return render(request, "main_page/verify_otp.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PromoCode, ManagerProfile
from .utils import send_whatsapp_promo_code
import random
import string


# Generate a unique promo code
def generate_unique_code(length=8):
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not PromoCode.objects.filter(code=code).exists():
            return code


# Step 1: Request OTP and generate promo code
@login_required
def generate_promo_code(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")

        if phone_number:
            otp = str(random.randint(100000, 999999))

            request.session["otp"] = otp
            request.session["otp_phone"] = phone_number

            success = send_whatsapp_promo_code(phone_number, otp)
            if success:
                messages.success(
                    request,
                    "OTP sent via WhatsApp. Please verify to receive your promo code.",
                )
                return redirect("verify_otp1")  # ✅ Changed this
            else:
                messages.error(request, "Failed to send OTP. Please try again.")

    return render(request, "main_page/generate_promo_code.html")


# Step 2: Verify OTP
@login_required
def verify_otp1(request):
    if request.method == "POST":
        input_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        phone_number = request.session.get("otp_phone")

        if input_otp == stored_otp:
            # Generate and store promo code
            code = generate_unique_code()
            PromoCode.objects.create(code=code, phone_number=phone_number, manager=None)
            messages.success(request, f"Promo code generated: {code}")
            return redirect("use_promo_code")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "main_page/verify_otp1.html")


# Step 3: Use promo code
@login_required
def use_promo_code(request):
    if request.method == "POST":
        promo_code = request.POST.get("promo_code")

        try:
            promo_instance = PromoCode.objects.get(code=promo_code, is_used=False)

            # Mark promo as used
            promo_instance.is_used = True
            promo_instance.used_by = request.user
            promo_instance.save()

            messages.success(request, "Promo code applied successfully!")
            return render(request, "main_page/promo_code_success.html")

        except PromoCode.DoesNotExist:
            messages.error(request, "Invalid or already used promo code.")

    return render(request, "main_page/use_promo_code.html")


#####################################swiggy##########


from django.utils.timezone import (
    now,
)  # Add this import statement at the top of the file
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FoodCategory, FoodItem


@login_required
def add_category(request):
    category_types = (
        FoodCategory.CATEGORY_TYPES
    )  # Get the category types from the model

    if request.method == "POST":
        name = request.POST["name"]
        category_type = request.POST.get(
            "category_type", ""
        )  # Get the selected category type
        image = request.FILES.get("image", None)

        user_data = {
            "user": request.user.username,
            "timestamp": now().isoformat(),
        }  # Store username & timestamp

        category = FoodCategory.objects.create(
            name=name,
            category_type=category_type,  # Store the selected category type
            image=image,
            user_name_Category=[user_data],  # Initialize with first entry
        )
        return redirect("vendor_dashboard")

    return render(
        request, "main_page/add_category.html", {"category_types": category_types}
    )  # Pass category_types to the template


# Add Food Item
@login_required
def add_food_item(request):
    if request.method == "POST":
        category_ids = request.POST.getlist("categories")  # Get multiple categories
        categories = FoodCategory.objects.filter(id__in=category_ids)

        name = request.POST["name"]
        description = request.POST["description"]
        price = request.POST["price"]
        discount = request.POST["discount"]
        image = request.FILES.get("image")
        food_type = request.POST["food_type"]

        if (
            not name
            or not description
            or not price
            or not discount
            or not image
            or not food_type
        ):
            return render(
                request,
                "main_page/add_food_item.html",
                {"error": "All fields are required", "categories": categories},
            )

        user_data = {
            "user": request.user.username,
            "timestamp": now().isoformat(),
        }  # Store username & timestamp

        food_item = FoodItem.objects.create(
            name=name,
            description=description,
            price=float(price),
            discount=float(discount),
            image=image,
            food_type=food_type,
            user_name_Food_item=[user_data],  # Initialize with first entry
        )
        food_item.categories.set(categories)

        return redirect("vendor_dashboard")

    categories = FoodCategory.objects.all()
    return render(request, "main_page/add_food_item.html", {"categories": categories})


# Edit Category
@login_required
def edit_category(request, category_id):
    category = get_object_or_404(FoodCategory, id=category_id)
    if request.method == "POST":
        category.name = request.POST["name"]
        if "image" in request.FILES:
            category.image = request.FILES["image"]

        # Append new user action
        user_data = {"user": request.user.username, "timestamp": now().isoformat()}
        category.user_name_Category.append(user_data)  # Append new data
        category.save()

        return redirect("vendor_dashboard")

    return render(request, "main_page/edit_category.html", {"category": category})


# Edit Food Item
@login_required
def edit_food_item(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    if request.method == "POST":
        category_ids = request.POST.getlist("categories")
        categories = FoodCategory.objects.filter(id__in=category_ids)

        food_item.name = request.POST["name"]
        food_item.description = request.POST["description"]
        food_item.price = request.POST["price"]
        food_item.discount = request.POST["discount"]
        food_item.food_type = request.POST["food_type"]

        if "image" in request.FILES:
            food_item.image = request.FILES["image"]

        # Append new user action
        user_data = {"user": request.user.username, "timestamp": now().isoformat()}
        food_item.user_name_Food_item.append(user_data)  # Append new data
        food_item.save()

        food_item.categories.set(categories)  # Update categories

        return redirect("vendor_dashboard")

    categories = FoodCategory.objects.all()
    return render(
        request,
        "main_page/edit_food_item.html",
        {"food_item": food_item, "categories": categories},
    )


# Delete Category
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(FoodCategory, id=category_id)
    category.delete()
    return redirect("vendor_dashboard")


# Delete Food Item
@login_required
def delete_food_item(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    food_item.delete()
    return redirect("vendor_dashboard")


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, Avg
from .models import FoodCategory, FoodItem, Order, OrderItem


@login_required
def vendor_dashboard(request):
    # Get the logged-in user (the vendor)
    user = request.user

    # Get all categories with their associated food items
    categories = FoodCategory.objects.prefetch_related("food_items").all()

    # Calculate the total sales amount, total sales quantity, and the number of orders
    order_items = OrderItem.objects.filter(order__user=user)

    # Total sales amount (sum of price_at_purchase * quantity for each order item)
    sales_amount = (
        order_items.aggregate(total_sales=Sum(F("price_at_purchase") * F("quantity")))[
            "total_sales"
        ]
        or 0
    )

    # Total sales quantity (sum of quantity for all order items)
    sales_quantity = (
        order_items.aggregate(total_quantity=Sum("quantity"))["total_quantity"] or 0
    )

    # Number of orders placed by the vendor (user)
    orders_count = Order.objects.filter(user=user).count()

    # Calculate overall rating for the food items the vendor has
    food_items = FoodItem.objects.filter(vendor=user)
    average_rating = food_items.aggregate(Avg("rating"))["rating__avg"] or 0

    # Prepare context to pass to template
    context = {
        "categories": categories,
        "sales_amount": sales_amount,
        "sales_quantity": sales_quantity,
        "average_rating": average_rating,
        "orders_count": orders_count,
    }

    # Render the vendor dashboard template with context
    return render(request, "main_page/vendor_dashboard1.html", context)

from .models import ManagerProfile

@login_required
def vendor_dashboard_by_shop(request, shop_id):
    user = request.user
    shop = get_object_or_404(ManagerProfile, id=shop_id, user=user)

    # You can now use `shop` to filter related FoodItems or Orders
    # Assuming FoodItems are linked to shop: food_items = FoodItem.objects.filter(shop=shop)
    # Add your logic here based on shop

    return render(request, "main_page/vendor_dashboard1.html", {
        "shop": shop,
        # Include other context data if needed
    })

# from django.shortcuts import render,get_object_or_404
# from .models import FoodCategory

# # Main page view
# def main_page(request):
#     food_categories = FoodCategory.objects.all()

#     context = {'food_categories': food_categories}
#     return render(request, "main_page/food_main_page.html", context)


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url="/main_page/login/")
def role_based_redirect(request):
    user = request.user

    if user.role == "manager":
        has_shop = ManagerProfile.objects.filter(user=user).exists()
        if has_shop:
            return redirect("vendor_dashboard")  # Manager with shop
        else:
            return redirect("register_shop")  # First-time manager
    elif user.role == "user":
        return main_page(request)  # Regular user
    else:
        return render(
            request, "main_page/access_denied.html", {"message": "Role not allowed."}
        )



from collections import defaultdict
from django.shortcuts import render
from .models import FoodCategory


def main_page(request):
    categories_by_type = defaultdict(list)

    for category in FoodCategory.objects.all():
        if category.category_type:
            categories_by_type[category.get_category_type_display()].append(category)

    context = {"categories_by_type": dict(categories_by_type)}
    return render(request, "main_page/food_main_page.html", context)


from django.shortcuts import render
from .models import FoodItem


def category_detail(request, category_id):
    """
    Displays food items belonging to a specific category.
    """
    category = get_object_or_404(FoodCategory, id=category_id)
    food_items = category.food_items.all()
    return render(
        request,
        "main_page/category_detail.html",
        {
            "category": category,
            "food_items": food_items,
        },
    )


from .models import FoodItem, PromoCode
from decimal import Decimal
from django.utils import timezone
from django.shortcuts import render
from django.http import JsonResponse
import json


def view_cart(request):
    if request.method == "POST":
        try:
            cart_data = json.loads(request.body)
            request.session["cart"] = cart_data
            return JsonResponse({"status": "success"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid cart data"}, status=400)

    # Handle remove item request (via GET for simplicity in this case)
    if "remove_item" in request.GET:
        food_id_to_remove = request.GET.get("remove_item")
        cart_data = request.session.get("cart", {})

        if food_id_to_remove in cart_data:
            del cart_data[food_id_to_remove]  # Remove the item from cart
            request.session["cart"] = cart_data  # Save updated cart to session

    cart_data = request.session.get("cart", {})
    promo_code_input = request.GET.get("promo_code", "").strip()

    items = []
    subtotal = Decimal("0.0")
    total_price = Decimal("0.0")  # After food-level discounts

    for food_id, quantity in cart_data.items():
        try:
            food_item = FoodItem.objects.get(id=food_id)
            price = food_item.price or Decimal("0.0")
            discount = food_item.discount or Decimal("0.0")

            item_total = price * quantity
            discounted_price = price - (price * discount / 100)
            discounted_total = discounted_price * quantity

            items.append(
                {
                    "food_id": food_id,  # Add food_id to the item for removal purposes
                    "name": food_item.name,
                    "price": price,
                    "quantity": quantity,
                    "discount": discount,
                    "total": discounted_total,
                }
            )

            subtotal += item_total
            total_price += discounted_total

        except FoodItem.DoesNotExist:
            continue

    # Promo code logic
    promo_discount = Decimal("0.0")
    applied_promo = None
    promo_error_message = None

    if promo_code_input:
        try:
            # Lookup promo code in a case-insensitive manner and ensure it hasn't been used
            promo = PromoCode.objects.get(code__iexact=promo_code_input, is_used=False)

            # Check if the current user has already used this promo code
            if promo.used_by and promo.used_by != request.user:
                raise ValueError(
                    "You have already used this promo code on a different account."
                )

            # Apply the promo discount based on a fixed value or percentage
            # If there is no discount field in PromoCode, you can apply some predefined value
            promo_discount = promo.promo_discount or Decimal(
                "0.0"
            )  # Adjust field name if needed

            # Calculate the discount amount and apply it
            discount_amount = total_price * (promo_discount / 100)
            total_price -= discount_amount
            applied_promo = promo

            # Mark the promo code as used and associate it with the user
            promo.is_used = True
            promo.used_by = request.user
            promo.save()

        except PromoCode.DoesNotExist:
            promo_error_message = (
                "Invalid promo code. Please check the code and try again."
            )
        except ValueError as e:
            promo_error_message = str(
                e
            )  # Capture any promo-related error (e.g., not valid yet or expired)

    return render(
        request,
        "main_page/cart.html",
        {
            "items": items,
            "subtotal": subtotal,
            "total_price": total_price,
            "promo_discount": promo_discount,
            "promo_code": applied_promo.code if applied_promo else None,
            "promo_error_message": promo_error_message,  # Display any errors
        },
    )


from django.shortcuts import render, redirect
from .models import Order, OrderItem
from django.http import JsonResponse
import json


def checkout(request):
    if request.method == "POST":
        cart_data = json.loads(request.body)  # Get cart data from the request

        # Create the order
        order = Order.objects.create(user=request.user, status="pending")

        total_price = 0.0

        # Loop through the cart data and create OrderItems
        for food_id, quantity in cart_data.items():
            try:
                food_item = FoodItem.objects.get(id=food_id)
                item_total = food_item.price * quantity
                total_price += item_total

                # Create an OrderItem for each item in the cart
                OrderItem.objects.create(
                    order=order,
                    food_item=food_item,
                    quantity=quantity,
                    price_at_purchase=food_item.price,
                )
            except FoodItem.DoesNotExist:
                continue

        # Update the total price of the order
        order.total_price = total_price
        order.save()

        # Return a JSON response with the order ID
        return JsonResponse({"order_id": order.id})

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FoodItem, Order, OrderItem
import json
from decimal import Decimal


def checkout_page(request):
    # Get cart from session
    cart_data = request.session.get("cart", {})
    items = []
    subtotal = Decimal("0.0")
    total_price = Decimal("0.0")

    for food_id, quantity in cart_data.items():
        try:
            food_item = FoodItem.objects.get(id=food_id)
            price = food_item.price or Decimal("0.0")
            discount = food_item.discount or Decimal("0.0")
            discounted_price = price - (price * discount / 100)
            discounted_total = discounted_price * quantity

            items.append(
                {
                    "name": food_item.name,
                    "quantity": quantity,
                    "price": price,
                    "discount": discount,
                    "total": discounted_total,
                }
            )

            subtotal += price * quantity
            total_price += discounted_total
        except FoodItem.DoesNotExist:
            continue

    return render(
        request,
        "main_page/checkout.html",
        {
            "items": items,
            "subtotal": subtotal,
            "total_price": total_price,
            "promo_code": request.GET.get("promo_code", ""),
            "promo_discount": 0,  # You can expand this logic to include promo codes if needed
        },
    )


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import FoodItem, Order, OrderItem
import json


@csrf_exempt
@login_required
def checkout(request):
    if request.method == "POST":
        try:
            # Load data from JSON
            data = json.loads(request.body)
            cart_data = data.get("cart", {})
            payment_method = data.get("payment_method", "Not Provided")

            # Create the order
            order = Order.objects.create(
                user=request.user,
                status="pending",  # Assuming payment is successful
                payment_method=payment_method,
                payment_status="paid",
            )

            total_price = Decimal("0.0")
            for food_id, quantity in cart_data.items():
                try:
                    food_item = FoodItem.objects.get(id=food_id)
                    item_total = food_item.price * quantity
                    total_price += item_total

                    OrderItem.objects.create(
                        order=order,
                        food_item=food_item,
                        quantity=quantity,
                        price_at_purchase=food_item.price,
                    )
                except FoodItem.DoesNotExist:
                    continue

            # Save total
            order.total_price = total_price
            order.save()

            # Clear the cart after successful order
            request.session["cart"] = {}

            return JsonResponse({"order_id": order.id})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)


from django.shortcuts import render, get_object_or_404
from .models import Order


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Get all order items
    items = order.order_items.select_related("food_item").all()

    return render(
        request,
        "main_page/order_detail.html",
        {
            "order": order,
            "items": items,
        },
    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order

# ================================
# USER VIEWS
# ================================


@login_required
def order_history(request):
    """View all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "main_page/order_history.html", {"orders": orders})


@login_required
def user_orders(request):
    """Specific view for users to see their orders."""
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "main_page/user_orders.html", {"orders": orders})


# ================================
# COOK VIEWS
# ================================


@login_required
def cook_orders(request):
    """View pending and cooking orders (for cooks)."""
    orders = Order.objects.filter(status__in=["pending", "cooking"]).order_by(
        "created_at"
    )
    return render(request, "main_page/cook_orders.html", {"orders": orders})


@login_required
def mark_order_cooked(request, order_id):
    """Update order status from pending -> cooking -> ready and assign cook."""
    order = get_object_or_404(Order, id=order_id)

    if order.status == "pending":
        order.status = "cooking"
        order.cook = request.user  # assign current user as cook
    elif order.status == "cooking":
        order.status = "ready"
    order.save()
    return redirect("cook_orders")


# ================================
# DELIVERY VIEWS
# ================================


@login_required
def delivery_orders(request):
    """View ready and delivering orders (for delivery personnel)."""
    orders = Order.objects.filter(status__in=["ready", "delivering"]).order_by(
        "created_at"
    )
    return render(request, "main_page/delivery_orders.html", {"orders": orders})


@login_required
def mark_ready_for_pickup(request, order_id):
    """Set delivery status to ready_for_pickup."""
    order = get_object_or_404(Order, id=order_id)
    if order.status == "ready":
        order.delivery_status = "ready_for_pickup"
        order.save()
    return redirect("delivery_orders")


@login_required
def mark_pickup_on_way(request, order_id):
    """Mark order as pickup_on_way and assign delivery person."""
    order = get_object_or_404(Order, id=order_id)
    if order.delivery_status == "ready_for_pickup":
        order.delivery_status = "pickup_on_way"
        order.delivery_person = request.user  # assign current user as delivery person
        order.status = "delivering"
        order.save()
    return redirect("delivery_orders")


@login_required
def mark_delivered(request, order_id):
    """Mark order and delivery status as delivered."""
    order = get_object_or_404(Order, id=order_id)
    if order.delivery_status == "pickup_on_way":
        order.delivery_status = "delivered"
        order.status = "delivered"
        order.save()
    return redirect("delivery_orders")


# views.py

from django.shortcuts import render
from .models import ManagerProfile


def local_market_shops(request):
    # Filter ManagerProfile objects where the shop is related to the "market" level (assuming you have a shop type/level field)
    market_shops = ManagerProfile.objects.filter(
        shop_number__isnull=False
    )  # You can filter based on your shop criteria
    return render(
        request, "main_page/local_market_shops.html", {"market_shops": market_shops}
    )


# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ManagerProfile
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import random


@login_required
def user_shop_list(request):
    shops = ManagerProfile.objects.all()  # Fetch all ManagerProfiles
    return render(request, "main_page/user_shop_list.html", {"shops": shops})


# View all local shops
@login_required
def manager_shop_list(request):
    shops = ManagerProfile.objects.all()  # Fetch all ManagerProfiles
    return render(request, "main_page/shop_list.html", {"shops": shops})


@login_required
def register_shop(request):
    # Prevent re-registration
    if ManagerProfile.objects.filter(user=request.user).exists():
        return redirect("manager_shop_list")

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        shop_photo = request.FILES.get("shop_photo")
        gst_number = request.POST.get("gst_number")
        shop_number = request.POST.get("shop_number")
        owner_aadhar_number = request.POST.get("owner_aadhar_number")
        owner_aadhar_photo = request.FILES.get("owner_aadhar_photo")
        selfie_with_shop = request.FILES.get("selfie_with_shop")

        # Create and save the new ManagerProfile
        new_shop = ManagerProfile(
            user=request.user,
            full_name=full_name,
            address=address,
            gender=gender,
            gst_number=gst_number,
            shop_number=shop_number,
            owner_aadhar_number=owner_aadhar_number,
            shop_photo=shop_photo,
            owner_aadhar_photo=owner_aadhar_photo,
            selfie_with_shop=selfie_with_shop,
        )
        new_shop.save()
        return redirect(
            "manager_shop_list"
        )  # Redirect to manager's list after registration

    return render(request, "main_page/register_shop.html")


@login_required
def update_shop(request, shop_id):
    shop = get_object_or_404(ManagerProfile, id=shop_id, user=request.user)
    if request.method == "POST":
        shop.full_name = request.POST.get("full_name", shop.full_name)
        shop.address = request.POST.get("address", shop.address)
        shop.gender = request.POST.get("gender", shop.gender)
        shop.gst_number = request.POST.get("gst_number", shop.gst_number)
        shop.shop_number = request.POST.get("shop_number", shop.shop_number)
        shop.owner_aadhar_number = request.POST.get(
            "owner_aadhar_number", shop.owner_aadhar_number
        )

        if "shop_photo" in request.FILES:
            shop.shop_photo = request.FILES["shop_photo"]
        if "owner_aadhar_photo" in request.FILES:
            shop.owner_aadhar_photo = request.FILES["owner_aadhar_photo"]
        if "selfie_with_shop" in request.FILES:
            shop.selfie_with_shop = request.FILES["selfie_with_shop"]

        shop.save()
        return redirect("manager_shop_list")

    return render(request, "main_page/update_shop.html", {"shop": shop})


@login_required
def delete_shop(request, shop_id):
    shop = get_object_or_404(ManagerProfile, id=shop_id, user=request.user)
    if request.method == "POST":
        shop.delete()
        return redirect("manager_shop_list")
    return render(request, "main_page/delete_shop.html", {"shop": shop})


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import ManagerProfile


@login_required
def shop_role_based_redirect(request):
    user = request.user

    if user.role == "manager":
        has_profile = ManagerProfile.objects.filter(user=user).exists()
        if has_profile:
            return redirect("manager_shop_list")  # Already registered
        else:
            return redirect("register_shop")  # First-time login, show registration
    else:
        return redirect("user_shop_list")  # Other roles go to general shop list













































####################################################








from django.shortcuts import render

# Create your views here.


def realtors_admin(request):
    return render(request, "main_page/realtors_admin.html")



# View for listing all realtors
def realtor_list(request):
    realtors = Realtor.objects.all()
    return render(request, "main_page/realtor_list.html", {"realtors": realtors})





# View for creating a new realtor
def realtor_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        is_mvp = request.POST.get("is_mvp") == "on"
        hire_date = datetime.now()

        # Handling file upload
        if request.FILES.get("photo"):
            photo = request.FILES["photo"]
            fs = FileSystemStorage()
            photo_path = fs.save(photo.name, photo)
        else:
            photo_path = None

        # Creating a new Realtor object
        realtor = Realtor(
            name=name,
            description=description,
            phone=phone,
            email=email,
            is_mvp=is_mvp,
            hire_date=hire_date,
            photo=photo_path,
        )
        realtor.save()
        return redirect("realtor_list")
    return render(request, "main_page/realtor_form.html")

from datetime import datetime
# View for editing an existing realtor
def realtor_edit(request, pk):
    realtor = get_object_or_404(Realtor, pk=pk)
    if request.method == "POST":
        realtor.name = request.POST.get("name")
        realtor.description = request.POST.get("description")
        realtor.phone = request.POST.get("phone")
        realtor.email = request.POST.get("email")
        realtor.is_mvp = request.POST.get("is_mvp") == "on"
        realtor.hire_date = datetime.now()

        # Handling file upload (if a new photo is uploaded)
        if request.FILES.get("photo"):
            photo = request.FILES["photo"]
            fs = FileSystemStorage()
            photo_path = fs.save(photo.name, photo)
            realtor.photo = photo_path

        realtor.save()
        return redirect("realtor_list")

    return render(request, "main_page/realtor_form.html", {"realtor": realtor})


# View for deleting a realtor
def realtor_delete(request, pk):
    realtor = get_object_or_404(Realtor, pk=pk)
    if request.method == "POST":
        realtor.delete()
        return redirect("realtor_list")
    return render(
        request, "main_page/realtor_confirm_delete.html", {"realtor": realtor}
    )


# List all listings
def listing_list(request):
    listings = Listing.objects.all()
    return render(request, "main_page/listing_list.html", {"listings": listings})


# Detail view of a single listing
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "main_page/listing_detail.html", {"listing": listing})


# Update an existing listing
@login_required  # Ensure that only logged-in users can update listings
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Ensure that only the realtor who created the listing can update it
    if listing.realtor != request.user.realtor:
        return HttpResponse(
            "You do not have permission to edit this listing.", status=403
        )

    if request.method == "POST":
        listing.title = request.POST.get("title")
        listing.description = request.POST.get("description")
        listing.price = request.POST.get("price")
        listing.bedrooms = request.POST.get("bedrooms")
        listing.bathrooms = request.POST.get("bathrooms")
        listing.garage = request.POST.get("garage")
        listing.sqft = request.POST.get("sqft")
        listing.lot_size = request.POST.get("lot_size")
        if "photo_main" in request.FILES:
            listing.photo_main = request.FILES.get("photo_main")
        listing.is_published = request.POST.get("is_published") == "on"

        listing.save()
        return redirect("listing_detail", pk=listing.pk)

    return render(request, "main_page/listing_update.html", {"listing": listing})


# Delete a listing
@login_required  # Ensure that only logged-in users can delete listings
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # Ensure that only the realtor who created the listing can delete it
    if listing.realtor != request.user.realtor:
        return HttpResponse(
            "You do not have permission to delete this listing.", status=403
        )

    if request.method == "POST":
        listing.delete()
        return redirect("listing_list")

    return render(
        request, "main_page/listing_confirm_delete.html", {"listing": listing}
    )



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
# from listings.models import Listing  # Ensure this import is correct based on your app structure
from .models import Listing
@login_required
def listing_create(request):
    if request.method == "POST":
        # Ensure user has an associated Realtor; if not, create one automatically
        realtor, created = Realtor.objects.get_or_create(user=request.user)

        # Proceed with listing creation as before
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        garage = request.POST.get("garage")
        sqft = request.POST.get("sqft")
        lot_size = request.POST.get("lot_size")
        photo_main = request.FILES.get("photo_main")
        is_published = request.POST.get("is_published") == "on"

        # Create the listing
        Listing.objects.create(
            realtor=realtor,
            title=title,
            description=description,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            garage=garage,
            sqft=sqft,
            lot_size=lot_size,
            photo_main=photo_main,
            is_published=is_published,
        )

        return redirect("listing_list")

    return render(request, "main_page/listing_create.html")
