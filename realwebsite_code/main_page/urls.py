from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    
    path("run-voice-assistant/", views.run_voice_assistant, name="run_voice_assistant"),

    path("", pre_home_screen, name="pre_home_screen"),
    path("create_coupon/", create_coupon, name="create_coupon"),
    path("coupon_list/", coupon_list, name="coupon_list"),
    path("claim/<int:coupon_id>/", claim_coupon, name="claim_coupon"),
    # User authentication
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout_view"),
    path("user_profile_view/", user_profile_view, name="user_profile"),
    path("manager_profile_view/", manager_profile_view, name="manager_profile"),
    path("coupon_dashboard_view", dashboard, name="dashboard"),
    path("register_view/", register_view, name="register_view"),
    path("request_login_otp/", request_login_otp, name="request_login_otp"),
    path("verify_login_otp/", verify_login_otp, name="verify_login_otp"),
    path("generate_promo_code/", generate_promo_code, name="generate_promo_code"),
    path("verify_otp/", verify_otp1, name="verify_otp1"),
    path("use_promo_code/", use_promo_code, name="use_promo_code"),
    ##############swiggy
    path("a", views.vendor_dashboard, name="vendor_dashboard"),
    path("swiggy/", main_page, name="main_page"),
    path("swiggy_dashboard/", views.role_based_redirect, name="role_based_redirect"),
    ##############swiggy_v
    path("add-category/", views.add_category, name="add_category"),
    path("add-food-item/", views.add_food_item, name="add_food_item"),
    path("edit-category/<int:category_id>/", views.edit_category, name="edit_category"),
    path(
        "delete-category/<int:category_id>/",
        views.delete_category,
        name="delete_category",
    ),
    path(
        "delete-food-item/<int:food_id>/",
        views.delete_food_item,
        name="delete_food_item",
    ),
    path("edit-food-item/<int:food_id>/", views.edit_food_item, name="edit_food_item"),
    path("checkout_page/", views.checkout_page, name="checkout_page"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("order_history/", views.order_history, name="order_history"),
    path(
        "cook/orders/mark_cooked/<int:order_id>/",
        views.mark_order_cooked,
        name="mark_order_cooked",
    ),
    
    
    
    path("cook/orders/", views.cook_orders, name="cook_orders"),
    path("delivery/orders/", views.delivery_orders, name="delivery_orders"),
    
    
    
    
    
    
    path(
        "order/<int:order_id>/mark-delivered/",
        views.mark_delivered,
        name="mark_delivered",
    ),
    path(
        "delivery/orders/ready_for_pickup/<int:order_id>/",
        views.mark_ready_for_pickup,
        name="mark_ready_for_pickup",
    ),
    path(
        "delivery/orders/pickup_on_way/<int:order_id>/",
        views.mark_pickup_on_way,
        name="mark_pickup_on_way",
    ),
    path(
        "delivery/orders/mark_delivered/<int:order_id>/",
        views.mark_delivered,
        name="mark_order_delivered",
    ),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "category/<int:category_id>/", views.category_detail, name="category_detail"
    ),  # Foods in a category
    path("local-market-shops/", views.local_market_shops, name="local_market_shops"),
    path(
        "shop_role_based_redirect",
        views.shop_role_based_redirect,
        name="shop_role_based_redirect",
    ),
    path("register_shop/", views.register_shop, name="register_shop"),
    path("user_shop_list/", views.user_shop_list, name="user_shop_list"),
    path("manager_shop_list/", views.manager_shop_list, name="manager_shop_list"),
    path("shop/<int:shop_id>/update/", views.update_shop, name="update_shop"),
    path("shop/<int:shop_id>/delete/", views.delete_shop, name="delete_shop"),
    path(
        "dashboard/shop/<int:shop_id>/",
        views.vendor_dashboard_by_shop,
        name="vendor_dashboard_by_shop",
    ),
    
    
    
    
    
    
    
    #########################################   RETALOR #########
    
    path('realtor_list', views.realtor_list, name='realtor_list'),
    
    path('create/', views.realtor_create, name='realtor_create'),
    path('edit/<int:pk>/', views.realtor_edit, name='realtor_edit'),
    path('delete/<int:pk>/', views.realtor_delete, name='realtor_delete'),
    path('listing_list', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/create/', views.listing_create, name='listing_create'),
    path('listing/update/<int:pk>/', views.listing_update, name='listing_update'),
    path('listing/delete/<int:pk>/', views.listing_delete, name='listing_delete'),
    
    path('listings', views.listings, name='listings'),
    path('<int:listing_id>', views.listing, name='listing'),
    path('search', views.search, name='search'),
    path('realtors_dashboard',views.realtors_admin,name ='realtors_admin'),
    
    
    
    
    
    
    path('retalor_role', views.retalor_role_based_redirect, name='retalor_role_based_redirect'), 
    path('realindex',views.realindex,name ='realindex'),
    path('about',views.about,name ='about'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
