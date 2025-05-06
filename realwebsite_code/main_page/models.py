from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
import random


# Custom User Model
class User(AbstractUser):
    # Role Choices
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (USER, "User"),
    ]

    # Level Choices
    ONLINE = "online"
    MARKET = "market"
    SPECIAL = "special"

    LEVEL_CHOICES = [
        (ONLINE, "Online"),
        (MARKET, "Market"),
        (SPECIAL, "Special"),
    ]

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=USER, null=True, blank=True
    )
    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, default=ONLINE, null=True, blank=True
    )

    # Rename reverse relationships to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return f"{self.username} ({self.role} - {self.level})"



# OTP Verification Model
class OTPVerification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return self.phone_number or "OTP Verification"


class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, default="")
    address = models.TextField(blank=True, default="")
    profile_photo = models.ImageField(upload_to="profiles/", blank=True, null=True)
    background_photo = models.ImageField(
        upload_to="backgrounds/", blank=True, null=True
    )
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class UserProfile(BaseProfile):
    def __str__(self):
        return self.full_name or f"UserProfile of {self.user.username}"


class ManagerProfile(BaseProfile):
    shop_photo = models.ImageField(upload_to="shop_photos/", blank=True, null=True)
    gst_number = models.CharField(max_length=15, blank=True, null=True)
    shop_number = models.CharField(max_length=20, blank=True, null=True)
    owner_aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    owner_aadhar_photo = models.ImageField(
        upload_to="aadhar_photos/", blank=True, null=True
    )
    selfie_with_shop = models.ImageField(
        upload_to="shop_selfies/", blank=True, null=True
    )

    def __str__(self):
        return self.full_name or f"ManagerProfile of {self.user.username}"


class Coupon(models.Model):
    CODE_LENGTH = 8

    LEVEL_CHOICES = [
        ("online", "Online"),
        ("market", "Market"),
        ("special", "Special"),
    ]

    image = models.ImageField(upload_to="coupon_images/", null=True, blank=True)

    code = models.CharField(max_length=CODE_LENGTH, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Required creator field
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_coupons",
    )

    # Optional creator info (if different from owner)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="coupons_created",
        null=True,
        blank=True,
    )

    level = models.CharField(
        max_length=10, choices=LEVEL_CHOICES, null=True, blank=True
    )

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return self.code or "Unnamed Coupon"


from django.conf import settings
class PromoCode(models.Model):
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    manager = models.OneToOneField(
        ManagerProfile, on_delete=models.CASCADE, null=True, blank=True
    )
    is_used = models.BooleanField(default=False, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    # ✅ Add this field to store the user who used the code
    used_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="used_promo_codes",
    )

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.code or "PromoCode"


from django.db import models
from django.contrib.auth.models import User


class FoodCategory(models.Model):
    CATEGORY_TYPES = [
        ("Food Options", "Food Options"),
        ("Shop Groceries on Instamart", "Shop Groceries on Instamart"),
        ("Restaurants", "Restaurants"),
        ("Special", "Special"),
        ("Festival", "Festival"),
    ]

    name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Allows name to be optional
    category_type = models.CharField(
        max_length=50, choices=CATEGORY_TYPES, null=True, blank=True
    )  # Allows null/blank
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    user_name_Category = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display() if self.category_type else 'No Type'})"


class FoodItem(models.Model):
    categories = models.ManyToManyField(
        FoodCategory, related_name="food_items", blank=True
    )  # Allows food items without categories
    name = models.CharField(
        max_length=100, null=True, blank=True
    )  # Allows name to be optional
    description = models.TextField(null=True, blank=True)  # Allows empty description
    price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Allows price to be optional
    image = models.ImageField(
        upload_to="food_images/", null=True, blank=True
    )  # Allows image to be optional
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Discount is optional
    FOOD_TYPE_CHOICES = [
        ("veg", "Veg"),
        ("non-veg", "Non-Veg"),
    ]
    food_type = models.CharField(
        max_length=7, choices=FOOD_TYPE_CHOICES, default="veg", null=True, blank=True
    )  # Allows null/blank
    user_name_Food_item = models.JSONField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True
    )  # Add a rating field for food items
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="food_items",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


# Order Model to track customer orders
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )  # Allows created_at to be optional
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Allows total price to be optional
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("cooking", "Cooking"),
        ("ready", "Ready"),
        ("Cooked_And_Delivered", "Cooked_And_Delivered"),
    )

    DELIVERY_STATUS_CHOICES = (
        ("ready_for_pickup", "Ready for Pickup"),
        ("pickup_on_way", "Pickup on the Way"),
        ("delivered", "Delivered"),
    )
    cook = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cooked_orders",
    )
    delivery_person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="delivered_orders",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    delivery_status = models.CharField(
        max_length=20, choices=DELIVERY_STATUS_CHOICES, default="ready_for_pickup"
    )

    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("COD", "Cash on Delivery"),
            ("Card", "Card"),
            ("UPI", "UPI"),
        ],
        null=True,
        blank=True,
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ],
        default="pending",
    )

    def __str__(self):
        return (
            f"Order #{self.id} by {self.user.username if self.user else 'Unknown User'}"
        )


# OrderItem to track food items in an order
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )  # Order is optional
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, null=True, blank=True
    )  # Food item is optional
    quantity = models.PositiveIntegerField(
        default=1, null=True, blank=True
    )  # Quantity is optional
    price_at_purchase = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Price is optional

    def __str__(self):
        return f"{self.food_item.name if self.food_item else 'Unknown Item'} (x{self.quantity})"


# Sales Report Model to help with easy retrieval of sales data (optional but helpful)
class SalesReport(models.Model):
    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, null=True, blank=True
    )  # Food item is optional
    total_sales_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # Allows total sales amount to be optional
    total_sales_quantity = models.PositiveIntegerField(
        null=True, blank=True
    )  # Allows total sales quantity to be optional
    total_orders = models.PositiveIntegerField(
        null=True, blank=True
    )  # Allows total orders to be optional

    def __str__(self):
        return f"Sales report for {self.food_item.name if self.food_item else 'Unknown Item'}"













from django.db import models
from django.conf import settings  # This will reference your custom User model
from datetime import datetime


class Realtor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Link to your custom User model
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __str__(self):
        return self.name or f"Realtor ({self.user.username})"




class Listing(models.Model):
  realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
  title = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  zipcode = models.CharField(max_length=20)
  description = models.TextField(blank=True)
  price = models.IntegerField()
  bedrooms = models.IntegerField()
  bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
  garage = models.IntegerField(default=0)
  sqft = models.IntegerField()
  lot_size = models.DecimalField(max_digits=5, decimal_places=1)
  photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
  photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  is_published = models.BooleanField(default=True)
  list_date = models.DateTimeField(default=datetime.now, blank=True)
  def __str__(self):
    return self.title