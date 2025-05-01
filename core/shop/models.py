from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from khayyam import JalaliDatetime
from random import randint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
import jdatetime
from django_jalali.db import models as jmodels
from datetime import date
from django.templatetags.static import static
from PIL import Image
from django.utils.text import slugify


def date2jalali(g_date):
	return jdatetime.date.fromgregorian(date=g_date) if g_date else None

class Policy(models.Model):
	delivery = models.TextField(default='توضیحات لازم در مورد شیوه‌های ارسال، مدت زمان انتظار و هزینه ارسال کالا', verbose_name='شیوه ارسال')
	payment = models.TextField(default='معرفی شیوه‌های پرداختی که در فروشگاه امکان‌پذیر است', verbose_name='شیوه‌های پرداخت')
	returns = models.TextField(default='توضیح صریح سیاست‌های مرجوعی و بازپرداخت وجه کالاهای عودت داده شده', verbose_name='سیاست‌های مرجوعی')
	rules_and_policies = models.TextField(default='قوانین و مقررات کلی سایت و سیاست‌های حریم خصوصی', verbose_name='قوانین و مقررات')

	class Meta:
		verbose_name = "قوانین و سیاست‌ها"
		verbose_name_plural = "قوانین و سیاست‌ها"

class Store(models.Model):
	name = models.CharField(max_length=250, unique=True, verbose_name='عنوان')
	is_active = models.BooleanField(default = False, verbose_name='فعال')
	address = models.CharField(max_length = 500, null=True, blank=True, verbose_name='آدرس')
	country = models.CharField(max_length = 250, default = 'iran', verbose_name='کشور')
	city = models.CharField(max_length = 250, default='tehran', verbose_name='شهر')
	about_description = models.TextField(default = "درباره فروشگاه، خدمات و سوابق آن", verbose_name='توضیحات')
	instagram = models.CharField(max_length=250, null=True, blank=True, verbose_name='اینستاگرام')
	telegram = models.CharField(max_length=250, null=True, blank=True, verbose_name='تلگرام')
	linkedin = models.CharField(max_length=250, null=True, blank=True, verbose_name='لینکدین')
	merchant = models.CharField(max_length=250, null=True, blank=True, verbose_name='مرچنت کد')
	phone_number = models.CharField(max_length = 250, null=True, blank = True, verbose_name='شماره تماس')
	email = models.EmailField(blank=True, verbose_name='ایمیل')
	# Layout_body = models.CharField(max_length = 250, default='app rtl light-mode scrollable-layout color-menu horizontal')
	# layout_sticky = models.CharField(max_length = 250, default = 'header sticky hor-header')
	# layout_container = models.CharField(max_length = 250, default= 'main-container container')
	color = models.CharField(max_length = 250, default = '0,0,0', verbose_name='رنگ اصلی')
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='تاریخ ایجاد')
	meta_description = models.TextField(default='فروشگاه اینترنتی ساخته شده با سایت ساز رایگان پیکوسایت', verbose_name='توضیحات متا')
	meta_keywords = models.TextField(default='ساخته شده با فروشگاه ساز پیکوسایت, فروشگاه اینترنتی, فروشگاه آنلاین, سایت ساز پیکوسایت', verbose_name='کلمات کلیدی')
	meta_og_title = models.TextField(default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت', verbose_name='عنوان OpenGrapg')
	meta_og_description = models.TextField( default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت', verbose_name='توضیحات OpenGrapg')
	meta_tc_title = models.TextField(default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت', verbose_name='عنوان کارت توییتر')
	meta_tc_description = models.TextField(default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت', verbose_name='توضیحات کارت توییتر')
	has_domain = models.BooleanField(default=False, verbose_name='دامنه فعال')
	has_payment_gw = models.BooleanField(default=False, verbose_name='درگاه پرداخت فعال')
	show_brands = models.BooleanField(default=False, verbose_name='نمایش برندها')
	template_index = models.IntegerField(default = 1, verbose_name='شماره قالب')
	index_title = models.CharField(max_length=250, null=True, blank=True, default='خانه', verbose_name='عنوان صفحه نخست')
	enamad_code = models.CharField(max_length=1000, null=True, blank=True, default='none', verbose_name='کد ای‌نماد')
	domain = models.CharField(max_length=250, null=True, blank=True, verbose_name='دامنه')
	show_advantages = models.BooleanField(default=True, verbose_name='نمایش نقاط قوت فروشگاه')
	show_featured_categories = models.BooleanField(default=True, verbose_name='نمایش دسته‌بندی‌های ویژه')
	show_special_offer = models.BooleanField(default=True, verbose_name='نمایش پیشنهادات شگفت‌انگیز')
	show_specials = models.BooleanField(default=True, verbose_name='نمایش محصولات ویژه')
	show_blog = models.BooleanField(default=True, verbose_name='نمایش وبلاگ')
	
	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ راه‌اندازی"

	def get_special_tags(self):
		return [tag for tag in Tag.objects.filter(is_special = True)]

	def get_special_tags_products(self):
		special_products = set()
		for tag in self.get_special_tags():
			tag_products = tag.get_products()
			for product in tag_products:
				special_products.add(product)
		return special_products

	def get_absolute_url(self):
		return reverse('shop:index')

	def get_logo_image(self):
		logo = StoreLogoImage.objects.all().first()
		if logo == None:
			logo_url = 'https://marketplace-bucket.storage.iran.liara.space/Picture1.png'
		else:
			logo_url = logo.image.url
		return logo_url
	
	def get_owner_name(self):
		owner = Owner.objects.all().first()
		return owner.full_name
	
	def get_owner_phone_number(self):
		owners_phone_numbers = []
		owners = Owner.objects.filter(store=self)
		return [owner.phone_number for owner in owners]

	def get_canonical(self):
		return f'https://picosite.ir/shop/{self.name}' 
	
	def get_payed_orders_num(self):
		payed_orders_num = 0
		for order in Order.objects.all():
			if order.status.latest_status == 'پرداخت شده' or order.status.latest_status == 'ارسال شده':
				payed_orders_num = payed_orders_num + 1
		return payed_orders_num
	
	def get_payed_orders_volume(self):
		payed_orders_volume = 0
		for order in Order.objects.all():
			if order.status.latest_status == 'پرداخت شده' or order.status.latest_status == 'ارسال شده':
				payed_orders_volume = payed_orders_volume + order.get_final_payment()
		return payed_orders_volume

	def get_brands(self):
		return Brand.objects.all()
	
	def __str__(self):
		return f'{self.name}'
	
	class Meta:
		verbose_name = "فروشگاه"
		verbose_name_plural = "فروشگاه"

class DefaultCategory(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True, verbose_name = 'دسته‌بندی مادر')
	is_sub = models.BooleanField(default=False, verbose_name = 'آیا زیردسته است؟')
	name = models.CharField(max_length=200, verbose_name = 'عنوان دسته')
	slug = models.SlugField(max_length=200, unique=True, verbose_name = 'نامک')

	class Meta:
		ordering = ('name',)
		verbose_name = 'دسته‌بندی‌های پیش‌فرض'
		verbose_name_plural = 'دسته‌بندی‌های پیش‌فرض'

	def __str__(self):
		return self.name

class PriceRange(models.Model):
	min_value = models.IntegerField(verbose_name='کمترین مقدار')
	max_value = models.IntegerField(verbose_name='بیشترین مقدار')

	class Meta:
		verbose_name = 'رنج‌های قیمتی'
		verbose_name_plural = 'رنج‌های قیمتی'

	def __str__(self):
		return f'{self.min_value} - {self.max_value} تومان'

class Customer(models.Model):
	phone_number = models.CharField(max_length = 11, verbose_name = 'شماره تماس')
	email = models.EmailField(null=True, blank=True, verbose_name = 'ایمیل')
	full_name = models.CharField(max_length = 250, default = 'کاربر میهمان', verbose_name = 'نام و نام خانوادگی')
	otp_token = models.IntegerField(null=True, blank= True, verbose_name = 'کد OTP')
	is_active = models.BooleanField(default=True, verbose_name = 'فعال')
	is_verified = models.BooleanField(default=False, verbose_name = 'تایید')
	city = models.CharField(max_length = 250, default = 'Tehran', verbose_name = 'شهر')
	zip_code = models.CharField(max_length = 10, default = '1234567890', verbose_name = 'کد پستی')
	address = models.TextField(default = 'نام محله - بلوار اصلی - خیابان اصلی - خیابان فرعی - کوچه - پلاک - واحد', verbose_name = 'آدرس')
	favorites = models.ManyToManyField('Product', blank=True, verbose_name = 'علاقمندی‌ها')
	created_date = models.DateTimeField(auto_now_add=True, null=True, blank = True, verbose_name = 'تاریخ ثبت‌نام')
	updated_date = models.DateTimeField(auto_now_add=True, null=True, blank = True, verbose_name = 'آخرین بروزرسانی')
	wallet_balance = models.IntegerField(default=0, null=True, blank=True, verbose_name = 'اعتبار کیف پول')

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ثبت‌نام"

	def get_total_purchase(self):
		status = OrderStatus.objects.get(id=1)
		orders = Order.objects.filter(customer=self, status=status)
		total_purchase = 0
		for order in orders:
			total_purchase = total_purchase + order.total_price
		return f'{total_purchase} تومان'

	def get_orders_count(self):
		status = OrderStatus.objects.get(id=1)
		orders_count = Order.objects.filter(customer=self, status=status).count()
		return orders_count
	
	class Meta:
		verbose_name = 'مشتریان'
		verbose_name_plural = 'مشتریان'

	
	def __str__(self):
		return self.phone_number
		
class Owner(models.Model):
	phone_number = models.CharField(max_length=11, verbose_name = 'شماره تماس')
	full_name = models.CharField(max_length=250, verbose_name = 'نام و نام خانوادگی')

	class Meta:
		verbose_name = 'مدیران فروشگاه'
		verbose_name_plural = 'مدیران فروشگاه'

	def __str__(self):
		return f'{self.full_name}'

class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, verbose_name='شماره تماس')
	code = models.PositiveSmallIntegerField(verbose_name='کد')
	created = models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد')

	class Meta:
		ordering = ['-created']
		verbose_name = 'کدهای OTP'
		verbose_name_plural = 'کدهای OTP'

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'	

class Delivery(models.Model):
	name = models.CharField(max_length = 250, verbose_name = 'عنوان')
	price = models.IntegerField( verbose_name = 'هزینه (تومان)')
	min_cart_free = models.IntegerField(default=2000000, verbose_name = 'حداقل مبلغ سبد برای ارسال رایگان') 
	min_cart_free_active = models.BooleanField(default=False, verbose_name = 'فعال بودن ارسال رایگان برای مبالغ بالا')

	class Meta:
		verbose_name = 'شیوه‌های ارسال'
		verbose_name_plural = 'شیوه‌های ارسال'

	def __str__(self):
		return f'{self.name} + {self.price} تومان '


class Tag(models.Model):
	name = models.CharField(max_length=200, verbose_name = 'عنوان')
	slug = models.CharField(max_length=200, verbose_name = 'نامک')
	is_special = models.BooleanField(default=False, verbose_name = 'تگ ویژه')

	class Meta:
		verbose_name = 'تگ‌ها'
		verbose_name_plural = 'تگ‌ها'

	def get_products(self):
		return self.product_set.all()

	def __str__(self):
		return f'{self.name} \n'

class Category(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True, verbose_name='دسته‌بندی مادر')
	is_sub = models.BooleanField(default=False, verbose_name='معرفی به عنوان زیردسته')
	name = models.CharField(max_length=200, verbose_name='عنوان')
	slug = models.SlugField(max_length=200, verbose_name='نامک')

	class Meta:
		ordering = ('name',)
		verbose_name = 'دسته‌بندی‌های محصولات'
		verbose_name_plural = 'دسته‌بندی‌های محصولات'	

	def get_absolute_url(self):
		return reverse('shop:category_products', kwargs={'category_slug':self.slug})

	def get_sub_categories(self):
		if self.is_sub == False:
			categories = Category.objects.filter(parent=self)
			return categories
		return None
	
	def get_products(self):
		return self.product_set.all()
	
	def get_category_brands(self):
		brands = []
		products = self.product_set.all()
		brands = set()
		for product in products:
			if product.brand:
				brands.add(product.brand)
		if self.get_sub_categories() != None:
			sub_categories = self.get_sub_categories()
			for sub_cat in sub_categories:
				products = sub_cat.product_set.all()
				for product in products:
					if product.brand:
						brand = product.brand
						brands.add(brand)
		return brands		

	def get_image_url(self):
		image = CategoryImage.objects.get(category=self)
		image_url = image.image.url
		return image_url
	
	def get_main_image(self):
		images = CategoryImage.objects.filter(category=self)
		main_image = images.first()
		if main_image == None:
			return static('assets/images/11.jpg')
		else:
			main_image_url = main_image.image.url
		return main_image_url

	def __str__(self):
		return f'{self.name}'
	
class Feature(models.Model):
	name = models.CharField(max_length = 250, verbose_name='عنوان')
	value = models.CharField(max_length = 250, verbose_name='مقدار')

	class Meta:
		verbose_name = 'ویژگی‌ها'
		verbose_name_plural = 'ویژگی‌ها'


class Product(models.Model):
	category = models.ManyToManyField(Category, verbose_name= 'دسته‌بندی')
	name = models.CharField(max_length=200, verbose_name = 'عنوان')
	slug = models.CharField(max_length=200, unique=True, blank=True, verbose_name = 'نامک')
	description = RichTextField(verbose_name = 'توضیحات')
	features = RichTextField(verbose_name = 'ویژگی‌ها')
	brand = models.ForeignKey('Brand', null=True, blank=True, on_delete=models.SET_NULL, verbose_name = 'برند')
	price = models.IntegerField(verbose_name = 'قیمت')
	sales_price = models.IntegerField(null=True, blank=True, verbose_name = 'قیمت تخفیف‌دار')
	off_active = models.BooleanField(default=False, verbose_name = 'فعال بودن فروش با تخفیف')
	tags = models.ManyToManyField(Tag, blank=True, verbose_name = 'تگ‌ها')
	created = models.DateTimeField(auto_now_add=True, verbose_name = 'تاریخ ایجاد')
	updated = models.DateTimeField(auto_now=True, verbose_name = 'آخرین بروزرسانی')
	views = models.IntegerField(default=0, verbose_name = 'بازدیدها')
	meta_description = models.TextField(null=True, blank=True, verbose_name = 'توضیحات متا')
	meta_keywords = models.TextField(null=True, blank=True, verbose_name = 'کلمات کلیدی')
	meta_og_title = models.TextField(null=True, blank=True, verbose_name = 'عنوان OpenGraph')
	meta_og_description = models.TextField(null=True, blank=True, verbose_name = 'توضیحات OpenGraph')
	meta_tc_title = models.TextField(null=True, blank=True, verbose_name = 'عنوان TwitterCard')
	meta_tc_description = models.TextField(null=True, blank=True, verbose_name = 'توضیحات TwitterCard')
	stock_alarm_volume = models.IntegerField(default=0, null=True, blank=True, verbose_name = 'هشدار اتمام موجودی')

	def get_normal_price(self):
		return "{:,}".format(self.price)
	
	def get_sales_price(self):
		return "{:,}".format(self.sales_price)

	def save(self, *args, **kwargs):
		# تولید اسلاگ فارسی با پشتیبانی از یونیکد
		self.slug = slugify(self.name, allow_unicode=True)
		super().save(*args, **kwargs)

	def get_varieties(self):
		return Variety.objects.filter(product = self)
	
	def show_varieties(self):
		varieties = Variety.objects.filter(product=self)
		return ", ".join([f"{variety.name} (Stock: {variety.stock})" for variety in varieties])	

	def get_stock_alarm_status(self):
		varieties = Variety.objects.filter(product = self)
		stock_volume = 0
		for variety in varieties:
			if variety.stock >= stock_volume:
				stock_volume = variety.stock
		if stock_volume <= self.stock_alarm_volume:
			stock_alarm_status = True
		else:
			stock_alarm_status = False
		return stock_alarm_status
		
	def get_default_meta_description(self):
		soup = BeautifulSoup(self.description, 'html.parser')
		raw_text = soup.get_text()
		return raw_text[0:160]
	
	def get_default_meta_keywords(self):
		store = Store.objects.all().first()
		return f'{store.name} - خرید {self.name}'
	
	def get_default_meta_og_title(self):
		store = Store.objects.all().first()
		return f'{store.name} - خرید {self.name}'
	
	def get_default_meta_og_description(self):
		soup = BeautifulSoup(self.description, 'html.parser')
		raw_text = soup.get_text()
		return raw_text[0:160]
	
	def get_default_meta_tc_title(self):
		store = Store.objects.all().first()
		return f'{store.name} - خرید {self.name}'
	
	def get_default_meta_tc_description(self):
		soup = BeautifulSoup(self.description, 'html.parser')
		raw_text = soup.get_text()
		return raw_text[0:160]
	
	def get_main_category(self):
		main_category = self.category.first()
		return main_category
	
	def get_brief_features(self):
		features = self.features
		lines = features.split('<br>')
		brief_features = lines[0:6]
		return brief_features

	def get_features_table(self):
		# جدا کردن خطوط
		lines = self.features.split('<br>')
		
		# شروع کد HTML
		feature_table = '<table>\n'
		
		# اضافه کردن هر خط به صورت یک سطر در جدول
		for line in lines:
			if ':' in line:
				title, value = line.split(':', 1)
				feature_table += f'  <tr>\n    <td style="width: 200px;">{title.strip()}</td>\n    <td>{value.strip()}</td>\n  </tr>\n'
		
		# پایان کد HTML
		feature_table += '</table>'
		
		return feature_table		

	class Meta:
		ordering = ('name',)
		verbose_name = 'محصولات'
		verbose_name_plural = 'محصولات'
		
	def get_main_image(self):
		images = ProductImage.objects.filter(product=self)
		main_image = images.first()
		if main_image == None:
			return static('assets/images/11.jpg')
		else:
			main_image_url = main_image.image.url
		return main_image_url

	def get_gallery(self):
		images = ProductImage.objects.filter(product=self)
		return images
	
	def get_selected_category_list(self):
		selected_cats = []
		for cat in self.category.all():
			selected_cats.append(cat.name)
		return selected_cats

	
	def get_active_price(self):
		if self.off_active == True and self.sales_price != None:
			active_price = self.sales_price
		else:
			active_price = self.price
		return "{:,}".format(active_price)

	def get_product_varieties(self):
		varieties = Variety.objects.filter(product = self)
		return varieties
	
	def get_stock_info(self):
		varieties = Variety.objects.filter(product = self)
		stock_info = {}
		for variety in varieties:
			stock_info[f'{variety.name}'] = variety.stock
		return stock_info
	
	def get_absolute_url(self):
		return reverse('shop:product_detail', kwargs={'product_slug':self.slug})

	def get_sell_stats(self):
		selled = 0
		for order in Order.objects.all():
			selled_items = order.get_selled_products()
			for item in selled_items:
				if item['product'] == self:
					selled = selled + item['quantity']
		return selled

	def get_related_products(self):
		related_products = set()
		product_categoreis = self.category.all()
		for cat in product_categoreis:
			if cat.is_sub == True:
				products = cat.product_set.all()
				for product in products:
					if product != self:
						related_products.add(product)
						if len(related_products)>=6:
							return list(related_products)
		for cat in product_categoreis:
			if cat.is_sub == False:
				products = cat.product_set.all()
				for product in products:
					if product != self:
						related_products.add(product)
						if len(related_products)>=6:
							return list(related_products)
		return list(related_products)

	def __str__(self):
		return f'{self.name} - id: {self.id}'
	
def image_upload_path(instance, filename):
	product_name = instance.product.name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{timestamp}_{filename}"
	return f"{product_name}/{filename}"

def logo_upload_path(instance, filename):
	logo_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{logo_name}_{filename}"
	return f"{filename}"

class ProductImage(models.Model):
	alt_name = models.CharField(max_length=2000, null=True, blank=True, verbose_name = 'نام جایگزین')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name = 'محصول')
	image = models.ImageField(upload_to=image_upload_path, default='media/11.png', verbose_name = 'تصویر')
	created = models.DateTimeField(auto_now_add=True, verbose_name = 'تاریخ ایجاد')

	class Meta:
		verbose_name = 'تصاویر محصولات'
		verbose_name_plural = 'تصاویر محصولات'
		ordering = ('created',)

	def get_absolute_url(self):
		return self.image.url

class StoreLogoImage(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='نام جایزگین')
	image = models.ImageField(upload_to=logo_upload_path, default='media/11.png', verbose_name='تصویر')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

	class Meta:
		ordering = ('created',)
		verbose_name = 'لوگوی فروشگاه'
		verbose_name_plural = 'لوگوی فروشگاه'

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

class Variety(models.Model):
	name = models.CharField(max_length=255, verbose_name='عنوان')
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
	stock = models.PositiveIntegerField(verbose_name='تعداد موجود در انبار')

	def __str__(self):
		return f'{self.product.name} - {self.name}'
	
	class Meta:
		verbose_name = 'تنوع محصولات'
		verbose_name_plural = 'تنوع محصولات'

class Comment(models.Model):
	sender = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='فرستنده')
	email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
	product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name='محصول')
	body = models.TextField(verbose_name='متن دیدگاه')
	approved = models.BooleanField(default=False, verbose_name='تایید نمایش')
	created_date = models.DateTimeField(auto_now_add = True, verbose_name='تاریخ ایجاد')

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

	class Meta:
		ordering = ('created_date',)
		verbose_name = 'دیدگاه‌ها'
		verbose_name_plural = 'دیدگاه‌ها'


class CartItem(models.Model):
	variety = models.ForeignKey(Variety, on_delete = models.CASCADE, null=True, blank=True, verbose_name='تنوع کالا')
	quantity = models.PositiveIntegerField(default = 1, verbose_name='تعداد')

	class Meta:
		verbose_name = 'آیتم‌های سبد خرید'
		verbose_name_plural = 'آیتم‌های سبد خرید'

	def __str__(self):
		return f'{self.variety.product.name} - id: {self.id} - تنوع: {self.variety.name} - تعداد: {self.quantity} عدد\n'

	def get_item_price(self):
		item_price = self.quantity*int(self.variety.product.get_active_price().replace(',',''))
		return f'{item_price:,}'

class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE, verbose_name='مشتری')
	items = models.ManyToManyField(CartItem, blank = True, verbose_name='آیتم‌های سبد خرید')

	class Meta:
		verbose_name = 'سبدهای خرید مشتریان'
		verbose_name_plural = 'سبدهای خرید مشتریان'

	def get_total_price(self):
		total_price = 0
		for item in self.items.all():
			total_price = total_price + int(item.get_item_price().replace(',',''))
		return "{:,}".format(total_price)
	
	def __str__(self):
		return f'{self.customer.phone_number}'

class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True, verbose_name="کد کوپن")
	start_date = jmodels.jDateField(verbose_name="تاریخ شروع", null=True, blank=True)
	end_date = jmodels.jDateField(verbose_name="تاریخ پایان", null=True, blank=True)
	discount = models.IntegerField(verbose_name="میزان تخفیف (تومان)", default=0)
	min_cart_volume = models.IntegerField(verbose_name="حداقل مبلغ سبد خرید (تومان)", default=0)

	class Meta:
		verbose_name = 'کدهای تخفیف'
		verbose_name_plural = 'کدهای تخفیف'

	def is_valid(self):
		"""بررسی می‌کند که آیا کوپن در بازه زمانی معتبر است یا نه."""
		today = date2jalali(date.today())  # تاریخ امروز به فرمت شمسی
		if self.start_date and self.end_date:
			return self.start_date <= today <= self.end_date
		elif self.start_date:
			return self.start_date <= today
		elif self.end_date:
			return today <= self.end_date
		return False

	def __str__(self):
		return self.code

class OrderStatus(models.Model):
	latest_status = models.CharField(max_length = 250, verbose_name='عنوان وضعیت')

	class Meta:
		verbose_name = 'وضعیت‌های سفارشات خرید'
		verbose_name_plural = 'وضعیت‌های سفارشات خرید'

	def __str__(self):
		return self.latest_status

class Cashback(models.Model):
	repetation = models.IntegerField(default=0, verbose_name='تکرار')
	percent = models.IntegerField(default=0, verbose_name='درصد')
	const = models.IntegerField(default=0, verbose_name='مقدار ثابت')

	class Meta:
		verbose_name = 'کش‌بک'
		verbose_name_plural = 'کش‌بک'

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='مشتری')
	items = models.ManyToManyField(CartItem, verbose_name='آیتم‌ها')
	total_price = models.IntegerField(verbose_name='مبلغ کل')
	status = models.ForeignKey(OrderStatus, on_delete = models.SET_NULL, null=True, verbose_name='وضعیت سفارش')
	created_date = models.DateTimeField(auto_now_add = True, verbose_name='تاریخ ایجاد')
	used_coupon = models.BooleanField(default=False, verbose_name='استفاده از کوپن تخفیف')
	delivery_method = models.ForeignKey(Delivery, on_delete = models.SET_NULL, null=True, blank=True, verbose_name='شیوه ارسال')
	status_updated_date = models.DateTimeField(auto_now_add = True, verbose_name='تاریخ بروزرسانی')
	reciever_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='نام تحویل گیرنده')
	reciever_familly_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='نام خانوادگی تحویل گیرنده')
	reciever_phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره تماس تحویل گیرنده')
	reciever_email = models.EmailField(max_length=250, null=True, blank=True, verbose_name='ایمیل تحویل گیرنده')
	reciever_state = models.CharField(max_length=250, null=True, blank=True, verbose_name='استان تحویل گیرنده')
	reciever_city = models.CharField(max_length=250, null=True, blank=True, verbose_name='شهر تحویل گیرنده')
	reciever_address = models.TextField(null=True, blank=True, verbose_name='آدرس تحویل گیرنده')
	reciever_zip_code = models.CharField(max_length=250, null=True, blank=True, verbose_name='کد پستی تحویل گیرنده')
	paid_by_wallet = models.IntegerField(default=0, verbose_name='میزان پرداخت با کیف پول')
	delivery_description = models.TextField(null=True, blank=True, verbose_name='توضیحات سفارش و ارسال')
	delivery_cost = models.IntegerField(default=0, verbose_name='هزینه ارسال')
	delivery_off = models.BooleanField(default=False, verbose_name='ارسال رایگان')

	def get_total_price(self):
		return f'{self.total_price:,}'

	class Meta:
		ordering = ('created_date',)
		verbose_name = 'سفارشات'
		verbose_name_plural = 'سفارشات'

	def get_raw_cost(self):
		orig_cost = 0
		for item in self.items.all():
			orig_cost = orig_cost + item.quantity*item.variety.product.price
		return f'{orig_cost:,}'
	
	def get_wallet_payment_volume(self):
		if self.delivery_method != None:
			total = self.delivery_method.price + self.total_price
		else:
			total = self.total_price
		wallet_payment = 0
		if self.customer.wallet_balance != 0:
			if total >= self.customer.wallet_balance:
				wallet_payment = self.customer.wallet_balance
			if self.customer.wallet_balance > total:
				wallet_payment = total
		return f'{wallet_payment:,}'
	
	def get_without_cashback_cost(self):
		if self.delivery_method != None:
			total = self.delivery_method.price + self.total_price
		else:
			total = self.total_price
		return f'{total:,}'

	def get_final_payment(self):
		if self.delivery_method != None:
			total = self.delivery_method.price + self.total_price
		else:
			total = self.total_price
		if self.customer.wallet_balance != 0:
			if total >= self.customer.wallet_balance:
				total = total - self.customer.wallet_balance
			else:
				total = 0
		return f'{total:,}'
	
	def get_selled_products(self):
		selled_products = []
		if self.status.latest_status == 'پرداخت شده':
			items = self.items.all()
			for item in items:
				quantity = item.quantity
				product = item.variety.product
				selled_products.append({
					'product': product,
					'quantity': quantity,
				})
		return selled_products
		
	def get_discount(self):
		orig_cost = 0
		for item in self.items.all():
			orig_cost = orig_cost + item.quantity*item.variety.product.price
		discount = orig_cost-self.total_price
		return f'{discount:,}'

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

	@property
	def shamsi_updated_date(self):
		return JalaliDatetime(self.status_updated_date).strftime('%Y/%m/%d')
	shamsi_updated_date.fget.short_description = "آخرین بروزرسانی"

class ContactMessage(models.Model):
	name = models.CharField(max_length=250, verbose_name='نام')
	familly_name = models.CharField(max_length=250, verbose_name='نام خانوادگی')
	email = models.EmailField(verbose_name='ایمیل')
	phone = models.CharField(max_length=11, verbose_name='شماره تماس')
	subject = models.CharField(max_length=250, verbose_name='موضوع')
	message = RichTextField(default = "پیام خود را وارد نمایید.", verbose_name='متن پیام')
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='تاریخ ارسال')
	is_answered = models.BooleanField(default = False, verbose_name='رسیدگی شده')

	class Meta:
		ordering = ('-created',)
		verbose_name = 'پیام‌ها'
		verbose_name_plural = 'پیام‌ها'

	def __str__(self):
		return f'{self.name} - {self.familly_name} - {self.subject}'
	
	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "آخرین ایجاد"

def slide_upload_path(instance, filename):
	slide_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
	filename = f"{slide_name}_{filename}"
	return f"{filename}"

class Slide(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان جایگزین')
	index = models.PositiveIntegerField(default=1, verbose_name='شماره اسلاید')
	image = models.ImageField(upload_to=slide_upload_path, default='media/11.png', verbose_name='تصویر')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
	tag = models.ManyToManyField(Tag, verbose_name='تگ محصولات هدف')
	category = models.ManyToManyField(Category, verbose_name='دسته‌بندی محصولات هدف')

	class Meta:
		ordering = ('created',)
		verbose_name = 'اسلایدها'
		verbose_name_plural = 'اسلایدها'

def banner_upload_path(instance, filename):
	banner_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{banner_name}_{filename}"
	return f"{filename}"

class Banner(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان جایگزین')
	index = models.PositiveIntegerField(default=1, verbose_name='شماره بنر')
	image = models.ImageField(upload_to=banner_upload_path, default='media/11.png', verbose_name='تصویر')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
	tag = models.ManyToManyField(Tag, blank=True, verbose_name='تگ محصولات هدف')
	category = models.ManyToManyField(Category, blank=True, verbose_name='دسته‌بندی محصولات هدف')
	size = models.CharField(max_length=250, default='small', verbose_name='سایز بنر')

	class Meta:
		ordering = ('created',)
		verbose_name = 'بنرها'
		verbose_name_plural = 'بنرها'

	def get_main_image(self):
		main_image = self.image
		if main_image == None:
			return static('assets/images/default_banner.jpg')
		else:
			main_image_url = main_image.url
		return main_image_url
	
class Faq(models.Model):
	question = models.CharField(max_length= 500, verbose_name='متن پرسش')
	answer = models.CharField(max_length=2000, verbose_name='متن پاسخ')

	class Meta:
		verbose_name = 'سوالات متداول'
		verbose_name_plural = 'سوالات متداول'

class WithdrawRecord(models.Model):
	sheba = models.CharField(max_length = 250, verbose_name='شماره شبا')
	amount = models.IntegerField(verbose_name='مبلغ به تومان')
	created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')
	is_paid = models.BooleanField(default=False, verbose_name='پرداخت شده')

	class Meta:
		ordering = ('-created_date',)
		verbose_name = 'درخواست‌های برداشت وجه'
		verbose_name_plural = 'درخواست‌های برداشت وجه'

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

	def __str__(self):
		return f'{self.amount} - {self.shamsi_created_date}'

class BlogCategory(models.Model):
	name = models.CharField(max_length=250, verbose_name='عنوان دسته‌بندی')

	class Meta:
		verbose_name = 'دسته‌بندی‌های مقالات'
		verbose_name_plural = 'دسته‌بندی‌های مقالات'

	def get_slug(self):
		return self.name.replace('/','').replace(' ','-')

	def __str__(self):
		return self.name

class BlogPost(models.Model):
	title = models.CharField(max_length=250, verbose_name='عنوان')
	slug = models.CharField(max_length = 250, verbose_name='نامک')
	category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name='دسته‌بندی')
	body = RichTextField(default = "insert the post body", verbose_name='متن مقاله')
	created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
	published = models.BooleanField(default=False, verbose_name='انتشار')
	meta_description = models.TextField(default='', verbose_name='توضیحات متا')
	meta_keywords = models.TextField(default='', verbose_name='کلمات کلیدی')
	meta_og_title = models.TextField(default= '', verbose_name='عنوان OpenGraph')
	meta_og_description = models.TextField( default= '', verbose_name='توضیحات OpenGraph')
	meta_tc_title = models.TextField(default= '', verbose_name='عنوان TwitterCard')
	meta_tc_description = models.TextField(default= '', verbose_name='توضیحات TwitterCard')

	class Meta:
		ordering = ('-created_date',)
		verbose_name = 'مقالات وبلاگ'
		verbose_name_plural = 'مقالات وبلاگ'

	def get_default_meta_description(self):
		return self.body[0:160]
	
	def get_default_meta_keywords(self):
		
		return f'{self.title} - {self.category.name}'
	
	def get_default_meta_og_title(self):
		return f'{self.title}'
	
	def get_default_meta_og_description(self):
		return self.body[0:160]
	
	def get_default_meta_tc_title(self):
		return f'{self.title}'
	
	def get_default_meta_tc_description(self):
		return self.body[0:160]
	
	def get_thumbnail(self):
		thumb = PostThumbnail.objects.filter(post=self).first()
		
		if thumb == None:
			thumbnail_url = 'https://marketplace-bucket.storage.iran.liara.space/shop/default-product-image.png'
		else:
			thumbnail_url = thumb.image.url
		return thumbnail_url

	def get_absolute_url(self):
		return reverse('shop:post_detail', kwargs={'post_slug':self.slug})
	
	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

def thumbnail_upload_path(instance, filename):
	thumbnail_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{thumbnail_name}_{filename}"
	return f"{filename}"

class PostThumbnail(models.Model):
	post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	image = models.ImageField(upload_to=thumbnail_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = 'لوگوی فروشگاه'
		verbose_name_plural = 'لوگوی فروشگاه'

class UploadedImages(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان دلخواه')
	image = models.ImageField(verbose_name='تصویر')

	class Meta:
		verbose_name = 'تصاویر آپلود شده'
		verbose_name_plural = 'تصاویر آپلود شده' 
		
def category_upload_path(instance, filename):
	category_name = instance.alt_name.replace(" ", "_")
	filename = f"{category_name}_{filename}"
	return f"{filename}"


class CategoryImage(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True, verbose_name='عنوان جایگزین')
	image = models.ImageField(upload_to=category_upload_path, default='media/11.png', verbose_name='تصویر')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته‌بندی')

	class Meta:
		ordering = ('-created',)
		verbose_name = 'تصویر دسته‌بندی'
		verbose_name_plural = 'تصویر دسته‌بندی'

	def get_absolute_url(self):
		return self.image.url
	
	def __str__(self):
		return f'تصویر دسته‌بندی {self.category.name}'

class FeaturedCategories(models.Model):
	categories = models.ManyToManyField(Category, blank=True, verbose_name='دسته‌بندی‌ها')

	class Meta:
		verbose_name = 'دسته‌بندی‌های شاخص'
		verbose_name_plural = 'دسته‌بندی‌های شاخص'

class Subscription(models.Model):
	email=models.EmailField(verbose_name='ایمیل')

	class Meta:
		verbose_name = 'اشتراک‌ها'
		verbose_name_plural = 'اشتراک‌ها'

def brand_upload_path(instance):
	logo_name = instance.name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{logo_name}"
	return f"{filename}"

class Brand(models.Model):
	name = models.CharField(max_length=250, verbose_name='نام برند')

	class Meta:
		verbose_name = 'برندها'
		verbose_name_plural = 'برندها'

	def __str__(self):
		return self.name

class Domain(models.Model):
	domain = models.CharField(max_length=100, verbose_name='نام دامنه')
	is_active = models.BooleanField(default=False, verbose_name='فعال')
	created_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

	class Meta:
		ordering = ('-created_date',)
		verbose_name = 'دامنه‌ی سایت'
		verbose_name_plural = 'دامنه‌ی سایت'

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

class Filter(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='دسته‌بندی')
	name = models.CharField(max_length=250, verbose_name='عنوان فیلتر')

	class Meta:
		verbose_name = 'فیلترهای دسته‌بندی‌های محصولات'
		verbose_name_plural = 'فیلترهای دسته‌بندی‌های محصولات'

	def get_values(self):
		return FilterValue.objects.filter(filter=self)

	def __str__(self):
		return f'{self.name}'
	
class FilterValue(models.Model):
	value = models.CharField(max_length=250, verbose_name='مقدار')	
	product = models.ForeignKey('Product',on_delete=models.CASCADE, related_name='filter_values', null=True, blank=True, verbose_name='محصول')  # اضافه کردن related_name
	filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=True, blank=True, verbose_name='عنوان فیلتر')

	class Meta:
		verbose_name = 'مقادیر فیلترها'
		verbose_name_plural = 'مقادیر فیلترها'

class ProductFilter(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
	filter = models.ForeignKey(Filter, on_delete=models.CASCADE, verbose_name='فیلتر')
	values = models.ManyToManyField(FilterValue, blank=True, verbose_name='مقدار فیلتر')

	class Meta:
		verbose_name = 'فیلترهای محصولات'
		verbose_name_plural = 'فیلترهای محصولات'

	def __str__(self):
		return f"{self.product.name} - {self.filter.name}"
	
class Announcement(models.Model):
	subject = models.CharField(max_length=250, blank = True, null=True, verbose_name='موضوع')
	message = models.TextField(verbose_name='متن اطلاعیه')
	is_active = models.BooleanField(default=True, verbose_name='فعال')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

	class Meta:
		ordering = ('-created',)
		verbose_name = 'اطلاعیه‌ها'
		verbose_name_plural = 'اطلاعیه‌ها'

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')
	shamsi_created_date.fget.short_description = "تاریخ ایجاد"

class Invoice(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice', verbose_name='سفارش')
	invoice_file = models.FileField(upload_to='invoices/', verbose_name='فایل فاکتور')
	created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

	class Meta:
		ordering = ('-created',)
		verbose_name = 'فاکتورها'
		verbose_name_plural = 'فاکتورها'



	def __str__(self):
		return f"فاکتور سفارش #{self.order.id}"
