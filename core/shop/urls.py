from django.urls import path, include
from . import views
from django.apps import apps

current_app_name = apps.get_containing_app_config(__name__).name



app_name = f"{current_app_name}"

urlpatterns = [
    
    path("api/v1/", include("shop.api.v1.urls")),
    path('', views.IndexView.as_view(), name='index'),
    path('owner/dashboard/edit-home/', views.HomePageUpdateView.as_view(), name='owner_dashboard_edit_home'),
    path('owner/dashboard/edit-layout/', views.ChangeThemeLayoutView.as_view(), name='owner_dashboard_edit_layout'),
    path('owner/dashboard/edit-home/categories/', views.GetFeaturedCategories.as_view(), name='owner_dashboard_edit_home_categories'),
    path('edit-home/add-slide/<int:index>', views.CreateSlideView.as_view(), name='add_slide'),
    path('edit-home/add-banner/<int:index>', views.CreateBannerView.as_view(), name='add_banner'),
    path('owner/', views.OwnerView.as_view(), name='owner'),
    path('owner-login/verify/<str:phone_number>/', views.VerifyOwnerView.as_view(), name='verify-owner'),
    path('owner/dashboard/announcements/', views.OwnerDashboardAnnouncements.as_view(), name ='owner_dashboard_announcements'),
    path('owner/dashboard/filters/', views.FilterView.as_view(), name = 'owner_dashboard_filters'),
    path('owner/dashboard/filters/edit-filter/<str:filter_id>/', views.EditFilterTitleView.as_view(), name = 'edit_filter'),
    path('owner/dashboard/filters/<int:filter_id>/delete/', views.DeleteFilter.as_view(), name = 'delete_filter'),
    path('owner/dashboard/products/duplicate/<int:product_id>', views.CopyProductView.as_view(), name = 'owner_dashboard_copy_product'),
    path('owner/dashboard/merchant-update/', views.SetMerchantCodeView.as_view(), name='owner_dashboard_merchant_update'),
    path('owner/dashboard/messages/<int:message_id>/answer/<int:status_id>', views.AnswerMessageView.as_view(), name='message_answer'),
    path('owner/dashboard/finance/', views.OwnerDashboardFinanceView.as_view(), name='owner_dashboard_finance'),
    path('owner/dashboard/delivery/', views.DeliveryListCreateView.as_view(), name='owner_dashboard_delivery'),
    path('owner/dashboard/coupons/', views.CouponListView.as_view(), name='owner_dashboard_coupons'),
    path('owner/dashboard/policies/', views.EditPoliciesView.as_view(), name='owner_dashboard_policies'),
    path('owner/dashboard/logo-update/', views.LogoUpdateView.as_view(), name='update_logo'),
    path('owner/dashboard/tickets/', views.TicketListView.as_view(), name='owner_dashboard_ticket_list'),
    path('owner/dashboard/ticket/create/', views.CreateTicketView.as_view(), name='owner_dashboard_create_ticket'),
    path('owner/dashboard/ticket/<str:ticket_id>/detail/', views.TicketDetailAndReplyView.as_view(), name='owner_dashboard_ticket_detail'),
    path('owner/dashboard/ticket/<str:ticket_id>/close/', views.CloseTicketView.as_view(), name='owner_dashboard_close_ticket'),

    path('owner/dashboard/blog-posts/', views.OwnerDashboardBlogView.as_view(), name='owner_dashboard_blog'),
    path('blog/post/create/', views.BlogPostCreateView.as_view(), name='create_blog_post'),
    path('blog/post/<str:post_slug>/edit/', views.BlogPostEditView.as_view(), name='edit_blog_post'),
    path('blog/post/<str:post_slug>/edit-meta/', views.PostMetaUpdateView.as_view(), name='edit_blog_post_meta_tags'),
    path('blog/post/<int:post_id>/thumbnail-update/', views.PostThumbnailUpdateView.as_view(), name='update_post_thumbnail'),

    path('owner/dashboard/blog-categories/', views.OwnerDashboardBlogCategoryView.as_view(), name='owner_dashboard_blog_category'),
    path('blog/category/create/', views.BlogCategoryCreateView.as_view(), name='create_blog_category'),
    path('blog/category/<int:blog_category_id>/edit/', views.BlogCategoryEditView.as_view(), name='edit_blog_category'),
    path('blog/category/<int:blog_category_id>/delete/', views.BlogCategoryDeleteView.as_view(), name='delete_blog_category'),

    path('customer/dashboard/', views.CustomerDashboardView.as_view(), name = 'customer_dashboard'),
    path('customer/dashboard/orders/', views.CustomerDashboardOrdersView.as_view(), name = 'customer_dashboard_orders'),
    path('customer/dashboard/orders/<int:order_id>/', views.CustomerDashboardOrderDatailView.as_view(), name = 'customer_dashboard_order_detail'),
    path('customer/dashboard/favorites/', views.CustomerDashboardFavoritesView.as_view(), name = 'customer_dashboard_favorites'),
    path('customer/dashboard/info/', views.CustomerDashboardInfoView.as_view(), name = 'customer_dashboard_info'),
    path('customer/dashboard/comments/', views.CustomerDashboardCommentsView.as_view(), name = 'customer_dashboard_comments'),

    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/tag/<str:tag_name>/', views.SpecialProductListView.as_view(), name='special_tag_products'),
    path('products/brand/<str:brand_name>/', views.BrandProductListView.as_view(), name='special_brand_products'),
    path('products/auto-dg/create/', views.AddProductFromDigikalaView.as_view(), name='add_product_from_dg'),

    path('delivery/<int:pk>/edit/', views.DeliveryEditView.as_view(), name='edit_delivery'),
    path('delivery/<int:pk>/delete/', views.DeliveryDeleteView.as_view(), name='delete_delivery'),

    path('owner/dashboard/tag/', views.TagListCreateView.as_view(), name='owner_dashboard_tag'),
    path('tag/<int:pk>/edit/', views.TagEditView.as_view(), name='edit_tag'),
    path('tag/<int:pk>/delete/', views.TagDeleteView.as_view(), name='delete_tag'),

    path('category/create/', views.CategoryCreateView.as_view(), name='create_category'),
    path('owner/dashboard/category/', views.CategoryListView.as_view(), name='owner_dashboard_categories'),
    path('owner/dashboard/category/delete-groupe/', views.DeleteCategoryGroupView.as_view(), name='owner_dashboard_categories_delete_groupe'),
    path('owner/dashboard/category/image/<int:category_id>/delete/', views.DeleteCategoryImageView.as_view(), name='delete_category_image'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='edit_category'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),
    
    path('customer-authentication/', views.CustomerRegisterLoginView.as_view(), name='customer_authentication'),
    path('customer-authentication/login/<str:phone_number>/', views.CustomerloginView.as_view(), name='customer-login'),
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('account/orders/', views.CustomerOrdersView.as_view(), name='customer-orders'),
    path('account/favorites/', views.CustomerFavoritesView.as_view(), name='customer-favorites'),
    # path('store-create/', views.StoreCreateView.as_view(), name='store-create'),    
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/tag/<str:tag_slug>/', views.FilterTagProducts.as_view(), name='filter_tag_products'),
    path('products/featured/<str:source>/', views.FeaturedProductListView.as_view(), name='featured_products'),
    path('products/category/<str:category_slug>/feature-filter/<str:form_name>/', views.FeatureFilterView.as_view(), name='feature_filter'),
    path('products/clear-active-filter/<str:filter_id>/<str:value_id>/', views.ClearActiveFilterValueView.as_view(), name='clear_active_filter'),
    path('add-to-favorites/<int:product_id>/<str:ref>/', views.AddToFavoritesView.as_view(), name='add_to_favorites'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('products/category/<str:category_slug>/', views.CategoryProductsListView.as_view(), name='category_products'),
    path('products/<str:product_slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<str:product_id>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:product_id>/asign_filter/', views.AsignFilterToProductView.as_view(), name='asign_filter'),
    path('products/<str:product_id>/delete-filter-value/<int:filter_value_id>/', views.DeleteFilterValueView.as_view(), name='delete_filter_value'),
    path('products/<str:product_slug>/update_meta/', views.ProductMetaTagsUpdateView.as_view(), name='edit_product_meta_tags'),
    path('products/<str:product_slug>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('products/add-to-cart/<int:pk>/', views.AddToCartView.as_view(), name='add_to_cart'),

    path('products/<int:pk>/image-upload/', views.UploadProductImagesView.as_view(), name='product_image_upload'),
    path('products/<str:product_id>/image/<str:image_id>/delete/', views.DeleteProductImageView.as_view(), name='product_image_delete'),
    # # path('product-images/', views.ProductImageCreateUpdateView.as_view(), name='product_image_list'),
    # # path('product-images/<int:product_image_id>/', views.ProductImageCreateUpdateView.as_view(), name='product_image_edit'),

    path('products/<int:product_id>/comments/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('owner/dashboard/comments/<int:comment_id>/approve/<int:status_id>', views.CommentApproveView.as_view(), name='comment_approve'),
    path('owner/dashboard/comments/', views.OwnerDashboardCommentsView.as_view(), name='owner_dashboard_comments'),

    path('cart/<int:cart_id>/', views.CartView.as_view(), name='cart_view'),
    path('cart/<int:cart_id>/update/<int:item_id>/', views.CartView.as_view(), name='cart_item_update'),
    path('cart/<int:cart_id>/delete/<int:item_id>/', views.DeleteCartItemView.as_view(), name='cart_item_delete'),
    path('create-order/', views.CreateOrderView.as_view(), name='create_order'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/<int:order_id>/update_status/<int:status_id>/', views.OrderProcessView.as_view(), name='update_order_status'),
    path('order-detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-reciever-detail/<int:order_id>/', views.RecieverDetailsView.as_view(), name='order_reciever_detail'),
    path('order-final-check/<int:order_id>/', views.OrderFinalCheckView.as_view(), name='order_final_check'),
    path('order-delivery-options/<int:order_id>/', views.OrderDeliveryOptionsView.as_view(), name='order_delivery_options'),
    path('order-detail/<int:order_id>/<str:wrong_code>', views.OrderWrongCouponView.as_view(), name='order_detail'),

    path('apply-coupon/<int:order_id>/coupon-apply', views.CouponApplyView.as_view(), name='apply_coupon'),
    path('apply-coupon/<int:order_id>/delivery-apply', views.DeliveryApplyView.as_view(), name='apply_delivery'),
    path('create-coupon/', views.CreateCouponView.as_view(), name='create_coupon'),
    path('delete-coupon/<int:coupon_id>', views.DeleteCouponView.as_view(), name='delete_coupon'),
    path('coupon-list/', views.CouponListView.as_view(), name='coupon_list'),
    path('about/', views.AboutUsPageView.as_view(), name='about'),
    path('contact/', views.ContactUsPageView.as_view(), name='contact'),
    path('faq/', views.FaqView.as_view(), name='faq_list'),
    path('policies/', views.PoliciesView.as_view(), name='policies'),
    path('owner/dashboard/faq/', views.FaqCreateView.as_view(), name='faq_create'),
    path('faq/edit/<int:faq_id>/', views.FaqUpdateView.as_view(), name='faq_update'),
    path('faq/delete/<int:faq_id>/', views.FaqDeleteView.as_view(), name='faq_delete'),

    path('blog/', views.BlogView.as_view(), name='post_list'),
    path('blog/<str:post_slug>/', views.BlogPostDetailView.as_view(), name='post_detail'),
    path('images/<str:image_class>/<int:index>/', views.ImageBankView.as_view(), name='image_bank'),
    path('images/<str:image_class>/<int:index>/<str:source>/<int:image_id>/', views.ApplyFromImageBankView.as_view(), name='apply_from_image_bank'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('order-payment/<int:order_id>/', views.OrderPayView.as_view(), name='order_payment'),
    path('orders/verify/', views.OrderVerifyView.as_view(), name='order_verify'),

    path('api/v1/', include('shop.api.v1.urls')),
    
   ]