from django.urls import path, include
from . import views
from django.apps import apps

current_app_name = apps.get_containing_app_config(__name__).name



app_name = f"{current_app_name}"

urlpatterns = [
    
    path("api/v1/", include("shop.api.v1.urls")),
    path('', views.IndexView.as_view(), name='index'),
    path('owner-login/verify/<str:phone_number>/', views.VerifyOwnerView.as_view(), name='verify-owner'),
    path('customer/dashboard/', views.CustomerDashboardView.as_view(), name = 'customer_dashboard'),
    path('customer/dashboard/orders/', views.CustomerDashboardOrdersView.as_view(), name = 'customer_dashboard_orders'),
    path('customer/dashboard/orders/<int:order_id>/', views.CustomerDashboardOrderDatailView.as_view(), name = 'customer_dashboard_order_detail'),
    path('customer/dashboard/favorites/', views.CustomerDashboardFavoritesView.as_view(), name = 'customer_dashboard_favorites'),
    path('customer/dashboard/info/', views.CustomerDashboardInfoView.as_view(), name = 'customer_dashboard_info'),
    path('customer/dashboard/comments/', views.CustomerDashboardCommentsView.as_view(), name = 'customer_dashboard_comments'),
    path('products/tag/<str:tag_name>/', views.SpecialProductListView.as_view(), name='special_tag_products'),
    path('products/brand/<str:brand_name>/', views.BrandProductListView.as_view(), name='special_brand_products'),
    path('products/auto-dg/create/', views.AddProductFromDigikalaView.as_view(), name='add_product_from_dg'),
    path('customer-authentication/', views.CustomerRegisterLoginView.as_view(), name='customer_authentication'),
    path('customer-authentication/login/<str:phone_number>/', views.CustomerloginView.as_view(), name='customer-login'),
    path('account/orders/', views.CustomerOrdersView.as_view(), name='customer-orders'),
    path('account/favorites/', views.CustomerFavoritesView.as_view(), name='customer-favorites'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/tag/<str:tag_slug>/', views.FilterTagProducts.as_view(), name='filter_tag_products'),
    path('products/featured/<int:featured_products_id>/', views.FeaturedProductListView.as_view(), name='featured_products'),
    path('products/special/<int:featured_products_id>/', views.SpecialProductsListView.as_view(), name='special_products'),
    path('products/category/<str:category_slug>/feature-filter/<str:form_name>/', views.FeatureFilterView.as_view(), name='feature_filter'),
    path('products/clear-active-filter/<str:filter_id>/<str:value_id>/', views.ClearActiveFilterValueView.as_view(), name='clear_active_filter'),
    path('add-to-favorites/<int:product_id>/<str:ref>/', views.AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('search/<str:search_item>/', views.SearchResultsView.as_view(), name='search_results'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('products/category/<str:category_slug>/', views.CategoryProductsListView.as_view(), name='category_products'),
    path('products/<str:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('products/<int:product_id>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('cart/<int:cart_id>/', views.CartView.as_view(), name='cart_view'),
    path('cart/<int:cart_id>/update/<int:item_id>/', views.CartView.as_view(), name='cart_item_update'),
    path('cart/<int:cart_id>/delete/<int:item_id>/', views.DeleteCartItemView.as_view(), name='cart_item_delete'),
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    path('order-detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-reciever-detail/<int:order_id>/', views.RecieverDetailsView.as_view(), name='order_reciever_detail'),
    path('order-final-check/<int:order_id>/', views.OrderFinalCheckView.as_view(), name='order_final_check'),
    path('order-detail/<int:order_id>/<str:wrong_code>', views.OrderWrongCouponView.as_view(), name='order_detail'),
    path('apply-coupon/<int:order_id>/coupon-apply', views.CouponApplyView.as_view(), name='apply_coupon'),
    path('about/', views.AboutUsPageView.as_view(), name='about'),
    path('contact/', views.ContactUsPageView.as_view(), name='contact'),
    path('faq/', views.FaqView.as_view(), name='faq_list'),
    path('policies/', views.PoliciesView.as_view(), name='policies'),
    path('blog/', views.BlogView.as_view(), name='post_list'),
    path('blog/category/<str:category_slug>/', views.CategoryBlogPostList.as_view(), name='category_post_list'),
    path('blog/<str:post_slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('order-payment/<int:order_id>/', views.OrderPayView.as_view(), name='order_payment'),
    path('orders/verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    path('api/v1/', include('shop.api.v1.urls')),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
   ]