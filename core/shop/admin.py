from django.contrib import admin
from.models import *
from django.utils.html import format_html
from django import forms
from django.contrib import admin
from .models import Product, Category
from utils import erase_stock_volume, update_slugs
import django_jalali.admin as jadmin
from django_jalali.admin.filters import JDateFieldListFilter
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.urls import path
from . import views
from django.contrib.auth.models import User, Group
from admin_interface.models import Theme


admin.site.unregister(Group)


class OtpCodeAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'code', 'shamsi_created_date')
	search_fields = ('phone_number',)

admin.site.register(OtpCode, OtpCodeAdmin)

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'payment', 'returns', 'rules_and_policies')
    search_fields = ('delivery', 'payment', 'returns', 'rules_and_policies')
    ordering = ('id',)

@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')  # ستون‌هایی که در لیست نمایش داده می‌شوند
    search_fields = ('name',)  # امکان جستجو براساس نام
    list_filter = ('category',)  # فیلتر بر اساس دسته‌بندی

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
	list_display = ('name', 'get_owner_name', 'phone_number', 'shamsi_created_date', 'has_domain', 'has_payment_gw')
	fields = ('name', 'is_active', 'address', 'country', 'city', 
			  'about_description', 'instagram', 'telegram', 'linkedin', 'merchant', 
			  'phone_number', 'email', 'color', 
			  'meta_description', 'meta_keywords', 'meta_og_title', 
			  'meta_og_description', 'meta_tc_title', 'meta_tc_description', 'has_domain', 'has_payment_gw',
			  'template_index', 'index_title', 'enamad_code','show_brands' ,'show_advantages','show_featured_categories','show_special_offer',
			  'show_specials','show_blog')

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'full_name')

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'min_cart_free')

# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
# 	list_display = ('subject','is_active', 'shamsi_created_date')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('parent', 'is_sub', 'name', 'slug')
	search_fields = ['name', 'slug']

class VarietyInline(admin.TabularInline):  # یا admin.StackedInline برای نمایش به صورت بلوکی
	model = Variety
	extra = 0  # تعداد فرم‌های اضافی
	fields = ('name', 'stock')  # فیلدهایی که می‌خواهید قابل ویرایش باشند
	can_delete = True  # در صورت نیاز به حذف کردن، این را به True تغییر دهید

def erase_stock(modeladmin, request, queryset):
	for product in queryset:
		erase_stock_volume(product)
	modeladmin.message_user(request, "The stock volume has been erased.")

# تعریف Inline برای تصاویر محصول
class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0
	fields = ('image', 'preview', 'alt_name')  # افزودن فیلد preview
	readonly_fields = ('preview',)  # فقط خواندنی بودن پیش‌نمایش

	def preview(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
		return "No Image"

	preview.short_description = "Image Preview"  # عنوان ستون در پنل ادمین

class FilterValueInline(admin.StackedInline):  # یا admin.TabularInline
	model = FilterValue
	extra = 1  # تعداد فرم‌های اضافی
	fields = ('filter', 'value')  # ترتیب نمایش فیلدها

# 2. Inline برای Filter
class FilterInline(admin.StackedInline):  # یا admin.TabularInline
	model = Filter
	extra = 1
	inlines = [FilterValueInline]  # اضافه کردن FilterValue به داخل Filter

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	change_list_template = 'shop/change_list.html'
	@admin.display(boolean=True, description='Stock Alarm')
	def stock_alarm(self, obj):
		return obj.get_stock_alarm_status()
	@admin.display(description='Active Price')
	def active_price(self, obj):
		return obj.get_active_price()
	list_display = ('name' ,'id','price','sales_price','off_active', 'active_price','brand' ,'stock_alarm')
	list_editable = ('price','off_active','sales_price')
	search_fields = ['name', 'slug']
	autocomplete_fields = ['category', 'tags']
	prepopulated_fields = {'slug': ('name',)}  
	inlines = [ProductImageInline, VarietyInline, FilterValueInline]

	actions = [erase_stock,update_slugs]

	# def view_on_site_icon(self, obj):
	# 	url = obj.get_absolute_url()  # اطمینان حاصل کنید متد get_absolute_url در مدل تعریف شده
	# 	return format_html('<a href="{}" target="_blank">View</a>', url)

	# view_on_site_icon.short_description = 'View on Site'  # عنوان ستون در ادمین
	# view_on_site_icon.allow_tags = True

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
# 	list_display = ('customer',)
# 	filter_horizontal = ('items',) 

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
	list_display = ('latest_status',)

# @admin.register(CartItem)
# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('variety', 'quantity')  # ستون‌هایی که در لیست نمایش داده می‌شوند
#     list_filter = ('variety',)  # امکان فیلتر کردن بر اساس فیلد variety
#     search_fields = ('variety__name',)  # امکان جستجو بر اساس نام variety

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('customer', 'total_price', 'status', 'shamsi_created_date', 'used_coupon', 'shamsi_updated_date')
	list_filter = ('status', 'used_coupon')
	search_fields = ['customer__full_name', 'status__latest_status']
	readonly_fields = ['items',]
	exclude = ('delivery_description',)
	

# @admin.register(Size)
# class SizeAdmin(admin.ModelAdmin):
# 	list_display = ['name']

@admin.register(PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
	list_display = ['min_value', 'max_value']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
	list_display = ('code', 'start_date', 'end_date', 'discount', 'min_cart_volume')
	list_filter = (
		('start_date', JDateFieldListFilter),
		('end_date', JDateFieldListFilter),
	)
	list_editable = ('start_date', 'end_date','discount', 'min_cart_volume')
	search_fields = ('code',)

class StoreLogoImageAdmin(admin.ModelAdmin):
	list_display = ('alt_name', 'shamsi_created_date')
	search_fields = ('alt_name',)

admin.site.register(StoreLogoImage, StoreLogoImageAdmin)


class ContactMessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'familly_name', 'email', 'phone', 'subject', 'shamsi_created_date')
	search_fields = ('name', 'familly_name', 'email', 'phone', 'subject')
	list_filter = ('subject',)

admin.site.register(ContactMessage, ContactMessageAdmin)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'is_special')
	search_fields = ['name', 'slug']


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
	list_display = ('index', 'alt_name', 'image_preview')
	search_fields = ['alt_name', ]
	autocomplete_fields = ['category', 'tag']

	def image_preview(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
		return "بدون تصویر"
	image_preview.short_description = "پیش‌نمایش تصویر"

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
	list_display = ('index', 'alt_name', 'image_preview', 'size')
	search_fields = ['alt_name',]
	autocomplete_fields = ['category', 'tag']

	def image_preview(self, obj):
		if obj.image:
			return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
		return "بدون تصویر"
	image_preview.short_description = "پیش‌نمایش تصویر"

@admin.register(Faq)
class FaqModelAdmin(admin.ModelAdmin):
	list_display = ('question', 'answer')
	search_fields = ['question', 'answer']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('sender', 'email', 'product', 'approved', 'shamsi_created_date')
	search_fields = ['sender', 'email', 'product__name', 'shamsi_created_date']
	list_filter = ('approved',)

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ['name']

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
	list_display = ('title', 'category', 'shamsi_created_date')
	search_fields = ['title', 'category__name', 'shamsi_created_date']
	list_filter = ('category',)

# @admin.register(UploadedImages)
# class UploadedImagesAdmin(admin.ModelAdmin):
# 	list_display = ('alt_name', 'image')
# 	search_fields = ['alt_name',]

class CategoryImageAdmin(admin.ModelAdmin):
	list_display = ('category', 'alt_name')
	search_fields = ('category__name', 'alt_name')
	list_filter = ('category', )

admin.site.register(CategoryImage, CategoryImageAdmin)

class FeaturedCategoriesAdmin(admin.ModelAdmin):
	list_display = ('display_categories',)

	def display_categories(self, obj):
		return ", ".join([category.name for category in obj.categories.all()])

	display_categories.short_description = 'Categories'

admin.site.register(FeaturedCategories, FeaturedCategoriesAdmin)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('email',)


class CustomerAdmin(admin.ModelAdmin):
	list_display = ('phone_number', 'email', 'full_name', 'is_active', 'is_verified', 'city', 'zip_code', 'shamsi_created_date', 'updated_date')
	search_fields = ['phone_number', 'full_name']
	autocomplete_fields = ['favorites',]

admin.site.register(Customer, CustomerAdmin)

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ['name']

# class TicketReplyInline(admin.TabularInline):
# 	model = TicketReply
# 	extra = 0

# class TicketAdmin(admin.ModelAdmin):
# 	list_display = ('subject', 'is_answered', 'is_closed', 'shamsi_created_date')
# 	inlines = [TicketReplyInline]

# admin.site.register(Ticket, TicketAdmin)

class DomainAdmin(admin.ModelAdmin):
	list_display = ('domain', 'is_active', 'shamsi_created_date')  # Add 'shamsi_created_date' to the list_display

admin.site.register(Domain, DomainAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'invoice_file', 'created')
    readonly_fields = ('created', )
    list_filter = ('created',)

admin.site.register(Invoice, InvoiceAdmin)











