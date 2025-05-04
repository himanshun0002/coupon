Here's a README.md for your Django project, based on the code you provided. It documents setup instructions, features, and usage:

🎟️ Coupon Sharing Platform - Django Web Application
This Django-based web application allows users and managers to register, log in, and create, claim, and manage coupons. The system distinguishes between user and manager roles and handles coupon creation, authentication, and profile management accordingly.

🚀 Features
User & Manager Registration with Role-Based Access

Login / Logout System

Create & View Coupons

Claim Coupons Based on User Level

Image Upload Support for Coupons and Profiles

Separate Profile Pages for Users

Promo Code Generation (redirects to generate_promo_code view)

🧾 Technologies Used
Python 3.x

Django 4.x+

SQLite (default DB)

HTML, CSS (Bootstrap recommended for templates)

Django Authentication System

📁 Project Structure
arduino
Copy
Edit
project/
│
├── main_page/
│   ├── templates/main_page/
│   │   ├── pre_home_screen.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── create_coupon.html
│   │   ├── coupon_list.html
│   │   └── user_profile.html
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── ...
├── manage.py
└── requirements.txt
🛠️ Setup Instructions
Clone the Repository

bash
Copy
Edit
git clone https://github.com/your-username/coupon-platform.git
cd coupon-platform
Create & Activate a Virtual Environment

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run Migrations

bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate
Create Superuser (Optional)

bash
Copy
Edit
python manage.py createsuperuser
Run the Development Server

bash
Copy
Edit
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

👤 Roles
User: Must upload an image while creating a coupon.

Manager: Can optionally upload an image, depending on a checkbox in the form.

📌 Key Views
View Function	URL Name	Description
pre_home_screen	pre_home_screen	Landing page after login
login_view	login	User login
register_view	register	New user registration
create_coupon	create_coupon	Create a new coupon
coupon_list	coupon_list	View all available coupons
claim_coupon	-	Claim a coupon if level matches
user_profile_view	user_profile	View and update user profile
logout_view	logout	Logout user

📦 Models (assumed from context)
User (Custom): Includes fields like username, email, password, role, level

Coupon: Fields include code, description, discount, valid_from, valid_to, owner, level, image, is_active

UserProfile, ManagerProfile: Additional user details like photos, address, etc.

✅ To Do / Suggestions
Add email verification or OTP system

Improve error handling and validations

Use Django Forms instead of raw request.POST access

Enhance UI with Bootstrap or Tailwind

Add generate_promo_code view

📃 License
This project is licensed under the MIT License.



Here's a comprehensive `README.md` for your Django project that covers the functionality you've implemented, including manager profiles, OTP-based login and promo code generation, food category and item management, and more:

---

# 🍽️ Fork & Pillow — Multi-Feature Django Web App

A robust Django-based platform supporting:

* 👤 User & Manager profiles
* 📞 WhatsApp-based OTP login and promo code verification
* 🧾 Promo Code claiming system
* 🍔 Vendor (Swiggy-style) food category/item management
* 📦 Dashboard for users & managers

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fork-and-pillow.git
cd fork-and-pillow
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser

```bash
python manage.py createsuperuser
```

### 5. Run the Server

```bash
python manage.py runserver
```

---

## 🔐 Authentication & Login

### ➕ OTP-Based Login via WhatsApp

* Users receive OTP via WhatsApp using a custom function `send_whatsapp_otp`.
* Two-step login:

  1. `/request_login_otp/` – Request OTP
  2. `/verify_login_otp/` – Verify and proceed to registration or login

### 👥 User Roles

* **User**: Basic customer profile via `UserProfile`
* **Manager**: Business/Shop owner with detailed registration via `ManagerProfile`

---

## 🧾 Manager Promo Code System

### 🔄 Flow:

1. Manager requests OTP to receive a promo code
2. OTP is sent via WhatsApp
3. Upon verification, a **unique promo code** is generated
4. Managers or users can apply the promo via `/use_promo_code/`

---

## 🍴 Vendor (Food) System

### 📂 Category Management

* Managers can create, edit categories with image uploads
* Each update logs timestamp and username

### 🍽️ Food Item Management

* Add/Edit food items with:

  * Name, description
  * Price, discount
  * Type (veg/non-veg/etc.)
  * Category linking (multiple supported)
  * Image
  * Logged user info and timestamp

---

## 📁 File Uploads

For **Manager Profiles**, the following file fields are supported:

* `profile_photo`
* `background_photo`
* `shop_photo`
* `owner_aadhar_photo`
* `selfie_with_shop`

---

## 📊 Dashboard

Customized dashboard at `/dashboard/` depending on user role:

* **User**: Shows basic info & owned coupons
* **Manager**: Shows registered details and shop assets

---

## 🗂️ Project Structure

```
main_page/
├── templates/main_page/
│   ├── dashboard.html
│   ├── request_otp.html
│   ├── verify_otp.html
│   ├── manager_profile.html
│   ├── generate_promo_code.html
│   ├── verify_otp1.html
│   ├── use_promo_code.html
│   ├── add_category.html
│   ├── add_food_item.html
│   ├── edit_category.html
│   └── edit_food_item.html
├── models.py
├── views.py
├── urls.py
└── utils.py  # send_whatsapp_otp, send_whatsapp_promo_code
```

---

## 📦 Dependencies

Make sure your `requirements.txt` includes:

```txt
Django>=3.2
pytz
whitenoise
Pillow
```

Add any other packages used for WhatsApp API (e.g., `pywhatkit`, `twilio`, etc.).

---

## 🛡️ Security Notes

* OTPs are stored temporarily in the session and verified manually
* Ensure HTTPS in production for secure transmission
* Limit OTP resend attempts to avoid abuse

---

## 🚀 Future Improvements

* JWT/Session-based OTP expiration
* QR-code-based shop verification
* Admin analytics dashboard
* Payment integration

---

Let me know if you'd like a custom badge set, project logo, or deployment guide (e.g., Heroku, Railway, AWS).



Here's a `README.md` that explains the structure and functionality of your Django views. You can include this in your project root directory to help collaborators or reviewers understand your codebase:

---

```markdown
# 🍽️ Fork & Pillow – Food Management System

This project enables food vendors and customers to interact via a web platform. It supports food categories, food items, order management, a vendor dashboard, promo codes, and cart functionality.

---

## 🚀 Features

- **Vendor Dashboard**
  - Displays food categories and items
  - Shows total sales amount, quantity, orders count, and average food item rating
- **Role-Based Redirection**
  - Redirects users based on their role (user or manager)
- **Food Category & Items**
  - Add, view, and delete food categories and items
- **Shop-Level Dashboard**
  - Each manager can view analytics for their shop
- **Cart System**
  - Add/remove items with dynamic price calculations
  - Promo code application with validation

---

## 🔒 Authentication

All dashboard and deletion routes are protected using `@login_required`.

---

## 📁 Views Overview

### `vendor_dashboard(request)`
- Aggregates sales data for the logged-in vendor.
- Template: `vendor_dashboard1.html`

### `vendor_dashboard_by_shop(request, shop_id)`
- Displays vendor dashboard stats for a specific shop (based on `ManagerProfile`).
- Template: `vendor_dashboard1.html`

### `delete_category(request, category_id)`
- Deletes a food category by ID.
- Redirects to `vendor_dashboard`.

### `delete_food_item(request, food_id)`
- Deletes a food item by ID.
- Redirects to `vendor_dashboard`.

### `role_based_redirect(request)`
- Redirects users to:
  - `vendor_dashboard` if they're a manager with a shop.
  - `register_shop` if they're a manager without a shop.
  - `main_page` if they're a regular user.

### `main_page(request)`
- Displays food categories grouped by their type.
- Template: `food_main_page.html`

### `category_detail(request, category_id)`
- Lists all food items under a selected category.
- Template: `category_detail.html`

### `view_cart(request)`
- Handles adding/removing items from the cart.
- Supports promo code application.
- Session-based cart data.
- Template: `cart.html`

---

## 🎁 Promo Code Logic

- Each promo code can only be used once per user.
- Applied only if not expired and not previously used.
- Discount is applied as a percentage reduction on the total cart value.

---

## 🗃️ Models Used (Referenced)

- `FoodCategory`
- `FoodItem`
- `Order`, `OrderItem`
- `ManagerProfile`
- `PromoCode`

---

## ✅ Prerequisites

- Django 4.x
- Python 3.x
- User authentication setup
- Models for food, orders, and user roles
- Templates in the `main_page/` directory

---

## ✏️ Contribution

Feel free to fork the project, raise issues, or create pull requests to improve the system!

---

## 🧑‍💻 Maintainer

Developed by **Himanshu Chauhan**

---
```

Would you like me to generate a matching folder structure or diagram for better visualization?


Here’s a structured and informative `README.md` file based on your Django food ordering and shop management platform:

---

# 🍽️ Fork & Pillow – Food Ordering and Local Market Shop Management System

## Overview

**Fork & Pillow** is a Django-based web platform for managing food orders and local market shops. It provides features for users to place orders, cooks to manage meal preparation, delivery personnel to track deliveries, and managers to register and update shop information.

---

## 🌟 Features

### 🧑‍🍳 User Features

* Browse local market shops
* View cart and checkout with promo code support
* View order history and order details

### 🍔 Food Ordering

* JSON-based cart checkout with real-time order creation
* Automated total price calculation including discount logic
* Order status updates: `pending`, `cooking`, `ready`, `delivering`, `delivered`

### 👨‍🍳 Cook Panel

* View `pending` and `cooking` orders
* Update order status and assign cook

### 🚚 Delivery Panel

* View `ready` and `delivering` orders
* Manage delivery statuses: `ready_for_pickup`, `pickup_on_way`, `delivered`

### 🏪 Shop Management

* Managers can:

  * Register a shop with photos and documents
  * Update shop information
  * View a list of their shops
  * Delete a shop profile

---

## 🔧 Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, Bootstrap
* **Database**: Default SQLite (customizable)
* **Authentication**: Django's built-in auth system
* **Session Handling**: For cart management
* **File Handling**: Django FileSystemStorage for shop registration documents

---

## 📁 Folder Structure (Partial)

```
main_page/
├── templates/
│   └── main_page/
│       ├── checkout.html
│       ├── order_detail.html
│       ├── order_history.html
│       ├── user_orders.html
│       ├── cook_orders.html
│       ├── delivery_orders.html
│       ├── shop_list.html
│       ├── register_shop.html
│       ├── update_shop.html
│       ├── delete_shop.html
│       └── local_market_shops.html
├── models.py
├── views.py
└── urls.py
```

---

## 🚀 How to Run

1. **Clone the repo**:

   ```bash
   git clone https://github.com/yourusername/fork-and-pillow.git
   cd fork-and-pillow
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run server**:

   ```bash
   python manage.py runserver
   ```

6. **Access app**:
   Open `http://127.0.0.1:8000/` in your browser.

---

## 🧑‍💼 Roles

* **User**: Places food orders, views shops.
* **Cook**: Prepares food orders, updates statuses.
* **Delivery**: Manages delivery flow from kitchen to customer.
* **Manager**: Registers and manages physical shop data.

---

## 📌 Notes

* Add promo code logic inside `checkout_page` to reflect real discounts.
* Ensure media handling is configured in `settings.py` for file uploads (shop photo, Aadhar photo, etc.).
* Admin can assign `user.role` manually or during registration logic.

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Create a pull request

---

## 📃 License

This project is licensed under the MIT License.

---

Would you like a `requirements.txt` or `settings.py` template added to this as well?
