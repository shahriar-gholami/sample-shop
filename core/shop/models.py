from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from datetime import date

from jalali_date import datetime2jalali, date2jalali
from khayyam import JalaliDatetime
from random import randint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
import datetime
from datetime import timedelta
from django_jalali.db import models as jmodels

class Store(models.Model):
	name = models.CharField(max_length=250, unique=True)
	is_active = models.BooleanField(default = False)
	active_days = models.PositiveIntegerField(default=0)
	address = models.CharField(max_length = 500, null=True, blank=True)
	country = models.CharField(max_length = 250, default = 'iran')
	city = models.CharField(max_length = 250, default='tehran')
	about_description = RichTextField(default = "درباره فروشگاه، خدمات و سوابق آن")
	instagram = models.CharField(max_length=250, null=True, blank=True)
	telegram = models.CharField(max_length=250, null=True, blank=True)
	linkedin = models.CharField(max_length=250, null=True, blank=True)
	merchant = models.CharField(max_length=250, null=True, blank=True)
	independent = models.BooleanField(default=False)
	phone_number = models.CharField(max_length = 250, null=True, blank = True)
	balance = models.IntegerField(default=0)
	email = models.EmailField(blank=True)
	Layout_body = models.CharField(max_length = 250, default='app rtl light-mode scrollable-layout color-menu horizontal')
	layout_sticky = models.CharField(max_length = 250, default = 'header sticky hor-header')
	layout_container = models.CharField(max_length = 250, default= 'main-container container')
	color = models.CharField(max_length = 250, default = '0,0,0')
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	meta_description = models.CharField(max_length=500, default='فروشگاه اینترنتی ساخته شده با سایت ساز رایگان پیکوسایت')
	meta_keywords = models.CharField(max_length=500, default='ساخته شده با فروشگاه ساز پیکوسایت, فروشگاه اینترنتی, فروشگاه آنلاین, سایت ساز پیکوسایت')
	meta_og_title = models.CharField(max_length=250, default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت')
	meta_og_description = models.CharField(max_length=1000, default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت')
	meta_tc_title = models.CharField(max_length=250, default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت')
	meta_tc_description = models.CharField(max_length=250, default= 'فروشگاه اینترنتی ساخته شده با پیکوسایت')
	has_domain = models.BooleanField(default=False)
	has_payment_gw = models.BooleanField(default=False)
	policies = RichTextField(default = "در این بخش مهم‌ترین سیاست‌های فروشگاه را ذکر نمایید. مهم‌ترین عناوین این بخش شامل سیاست‌های مرجوعی و شیوه‌ها و بازه زمانی ارسال کالا می‌باشند.")
	template_index = models.IntegerField(default = 1)
	index_title = models.CharField(max_length=250, null=True, blank=True, default='خانه')
	enamad_code = models.CharField(max_length=1000, null=True, blank=True, default='none')
	domain_msg = models.BooleanField(default=False)
	gw_msg = models.BooleanField(default=False)
	has_notif = models.BooleanField(default=False)

	
	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')

	def get_special_tags(self):
		return [tag for tag in Tag.objects.filter(is_special = True)]

	def get_special_tags_products(self):
		special_products = []
		for tag in self.get_special_tags():
			tag_products = tag.get_products()
			for product in tag_products:
				special_products.append(product)
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

class DefaultCategory(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
	is_sub = models.BooleanField(default=False)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

class Size(models.Model):
	name = models.CharField(max_length=250)

class PriceRange(models.Model):
	min_value = models.IntegerField()
	max_value = models.IntegerField()

	def __str__(self):
		return f'{self.min_value} - {self.max_value} تومان'

class Customer(models.Model):
	phone_number = models.CharField(max_length = 11)
	email = models.EmailField(null=True, blank=True)
	full_name = models.CharField(max_length = 250, default = 'کاربر میهمان')
	otp_token = models.IntegerField(null=True, blank= True)
	is_active = models.BooleanField(default=True)
	is_verified = models.BooleanField(default=False)
	city = models.CharField(max_length = 250, default = 'Tehran')
	zip_code = models.CharField(max_length = 10, default = '1234567890')
	address = models.CharField(max_length = 250, default = 'نام محله - بلوار اصلی - خیابان اصلی - خیابان فرعی - کوچه - پلاک - واحد')
	favorites = models.ManyToManyField('Product', blank=True)
	created_date = models.DateTimeField(auto_now_add=True, null=True, blank = True)
	updated_date = models.DateTimeField(auto_now_add=True, null=True, blank = True)
	wallet_balance = models.IntegerField(default=0, null=True, blank=True)

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

	
	def __str__(self):
		return self.phone_number
		
class Owner(models.Model):
	phone_number = models.CharField(max_length=11)
	full_name = models.CharField(max_length=250)

	def __str__(self):
		return f'{self.full_name}'

class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'	

class Delivery(models.Model):
	name = models.CharField(max_length = 250)
	price = models.IntegerField()
	min_cart_free = models.IntegerField(default=2000000) 
	min_cart_free_active = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name} + {self.price} تومان '


class Tag(models.Model):
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=200)
	is_special = models.BooleanField(default=False)

	def get_products(self):
		return self.product_set.all()

	def __str__(self):
		return f'{self.name} \n'

class Category(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
	is_sub = models.BooleanField(default=False)
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'	

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
				brand = Brand.objects.get(name = product.brand)
				brands.add(brand)
		if self.get_sub_categories() != None:
			sub_categories = self.get_sub_categories()
			for sub_cat in sub_categories:
				products = sub_cat.product_set.all()
				for product in products:
					if product.brand:
						brand = Brand.objects.get(name = product.brand)
						brands.add(brand)
		return brands		

	def get_image_url(self):
		image = CategoryImage.objects.get(category=self)
		image_url = image.image.url
		return image_url

	def __str__(self):
		return f'{self.name}'
	
class Feature(models.Model):
	name = models.CharField(max_length = 250)
	value = models.CharField(max_length = 250)
	
class ProductRefClass(models.Model):
	name = models.CharField(max_length=250)
	price_coef = models.IntegerField(default=100)

	def __str__(self):
		return self.name

class ProductColor(models.Model):
	name = models.CharField(max_length=250)
	color_code = models.CharField(max_length=250)

	def __str__(self):
		return self.name

class Product(models.Model):
	category = models.ManyToManyField(Category)
	name = models.CharField(max_length=200)
	slug = models.CharField(max_length=200, )
	description = RichTextField()
	features = RichTextField()
	brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
	price = models.IntegerField()
	sales_price = models.IntegerField(null=True, blank=True)
	off_active = models.BooleanField(default=False)
	tags = models.ManyToManyField(Tag, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	views = models.IntegerField(default = 0)
	meta_description = models.CharField(max_length=500, null=True, blank = True)
	meta_keywords = models.CharField(max_length=500, null=True, blank = True)
	meta_og_title = models.CharField(max_length=250,  null=True, blank = True)
	meta_og_description = models.CharField(max_length=1000,  null=True, blank = True)
	meta_tc_title = models.CharField(max_length=250,  null=True, blank = True)
	meta_tc_description = models.CharField(max_length=250,  null=True, blank = True)
	ref_class = models.ForeignKey(ProductRefClass, null=True, blank=True, on_delete=models.SET_NULL)
	ref_price = models.IntegerField(default=0, null=True, blank=True)
	stock_alarm_volume = models.IntegerField(default=0, null=True, blank=True)
	verified = models.BooleanField(default=False)
	express = models.BooleanField(default=False)

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
		verbose_name = "محصول"
		verbose_name_plural = "محصولات"

	def get_main_image(self):
		images = ProductImage.objects.filter(product=self)
		main_image = images.first()
		if main_image == None:
			main_image_url = 'https://marketplace-bucket.storage.iran.liara.space/shop/default-product-image.png'
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
	
	def get_class_price(self):
		class_price = self.ref_price * self.ref_class.price_coef /100
		return class_price
	
	def get_active_price(self):
		if self.ref_class == None:
			if self.off_active == True and self.sales_price != None:
				active_price = self.sales_price
			else:
				active_price = self.price
		else:
			if self.off_active == True and self.sales_price != None:
				active_price = self.sales_price
			else:
				active_price = self.ref_price*self.ref_class.price_coef/100
		return active_price

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
		return f'{self.name}'
	
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
	alt_name = models.CharField(max_length=2000, null=True, blank=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	custom_name = models.CharField(max_length=2000, blank=True, null=True)
	image = models.ImageField(upload_to=image_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created',)

	def get_absolute_url(self):
		return self.image.url

	def save(self, *args, **kwargs):
		if not self.custom_name:
			product_name = self.product.name.replace(" ", "_")
			timestamp = timezone.now().strftime("%Y%m%d")
			self.custom_name = f"{product_name}_{timestamp}"
		super().save(*args, **kwargs)

class StoreLogoImage(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	custom_name = models.CharField(max_length=250, blank=True, null=True)
	image = models.ImageField(upload_to=logo_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		if not self.custom_name:
			timestamp = timezone.now().strftime("%Y%m%d")
			self.custom_name = f"{timestamp}"
		super().save(*args, **kwargs)

class Variety(models.Model):
	name = models.CharField(max_length=255)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	stock = models.PositiveIntegerField()

	def __str__(self):
		return f'{self.product.name} - {self.name}'

class Comment(models.Model):
	sender = models.ForeignKey(Customer, on_delete=models.CASCADE)
	email = models.EmailField(null=True, blank=True)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	body = models.TextField()
	approved = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add = True)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

class CartItem(models.Model):
	variety = models.ForeignKey(Variety, on_delete = models.CASCADE, null=True, blank=True)
	quantity = models.PositiveIntegerField(default = 1)

	def get_item_price(self):
		item_price = self.quantity*self.variety.product.get_active_price()
		return item_price

class Cart(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
	items = models.ManyToManyField(CartItem, blank = True)

	def get_total_price(self):
		total_price = 0
		for item in self.items.all():
			total_price = total_price + item.get_item_price()
		return total_price
	
	def __str__(self):
		return f'{self.customer.phone_number}'

class Coupon(models.Model):
	code = models.CharField(max_length=50, unique=True, verbose_name="کد کوپن")
	start_date = jmodels.jDateField(verbose_name="تاریخ شروع", null=True, blank=True)
	end_date = jmodels.jDateField(verbose_name="تاریخ پایان", null=True, blank=True)
	discount = models.IntegerField(verbose_name="میزان تخفیف (تومان)", default=0)
	min_cart_volume = models.IntegerField(verbose_name="حداقل مبلغ سبد خرید (تومان)", default=0)

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
	latest_status = models.CharField(max_length = 250)

	def __str__(self):
		return self.latest_status

class Cashback(models.Model):
	repetation = models.IntegerField(default=0)
	percent = models.IntegerField(default=0)
	const = models.IntegerField(default=0)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
	items = models.ManyToManyField(CartItem)
	total_price = models.IntegerField()
	status = models.ForeignKey(OrderStatus, on_delete = models.SET_NULL, null=True)
	created_date = models.DateTimeField(auto_now_add = True)
	used_coupon = models.BooleanField(default=False)
	delivery_method = models.ForeignKey(Delivery, on_delete = models.SET_NULL, null=True, blank=True)
	status_updated_date = models.DateTimeField(auto_now_add = True)
	reciever_name = models.CharField(max_length=250, null=True, blank=True)
	reciever_familly_name = models.CharField(max_length=250, null=True, blank=True)
	reciever_phone_number = models.CharField(max_length=11, null=True, blank=True)
	reciever_email = models.EmailField(max_length=250, null=True, blank=True)
	reciever_state = models.CharField(max_length=250, null=True, blank=True)
	reciever_city = models.CharField(max_length=250, null=True, blank=True)
	reciever_address = models.CharField(max_length=250, null=True, blank=True)
	reciever_zip_code = models.CharField(max_length=250, null=True, blank=True)
	paid_by_wallet = models.IntegerField(default=0)
	has_express_items = models.BooleanField(default=False)
	has_normal_items = models.BooleanField(default=False)
	delivery_description = models.TextField(null=True, blank=True)
	delivery_cost = models.IntegerField(default=0)
	delivery_off = models.BooleanField(default=False)

	def get_raw_cost(self):
		orig_cost = 0
		for item in self.items.all():
			orig_cost = orig_cost + item.quantity*item.variety.product.price
		return orig_cost
	
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
		return wallet_payment
	
	def get_without_cashback_cost(self):
		if self.delivery_method != None:
			total = self.delivery_method.price + self.total_price
		else:
			total = self.total_price
		return total

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
		return total
	
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

	def get_order_express_products(self):
		order_express_products = []
		selled_products = []
		items = self.items.all()
		for item in items:
			product = item.variety.product
			selled_products.append(product)
		for product in selled_products:
			if product.express == True:
				order_express_products.append(product)
		return order_express_products

	def get_order_normal_products(self):
		order_normal_products = []
		selled_products = []
		items = self.items.all()
		for item in items:
			product = item.variety.product
			selled_products.append(product)
		for product in selled_products:
			if product.express == False:
				order_normal_products.append(product)
		return order_normal_products
		
	def get_discount(self):
		orig_cost = 0
		for item in self.items.all():
			orig_cost = orig_cost + item.quantity*item.variety.product.price
		discount = orig_cost-self.total_price
		return discount

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

class ContactMessage(models.Model):
	name = models.CharField(max_length=250)
	familly_name = models.CharField(max_length=250)
	email = models.EmailField()
	phone = models.CharField(max_length=11)
	subject = models.CharField(max_length=250)
	message = RichTextField(default = "پیام خود را وارد نمایید.")
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	is_answered = models.BooleanField(default = False)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return f'{self.name} - {self.familly_name} - {self.subject}'

def slide_upload_path(instance, filename):
	slide_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
	filename = f"{slide_name}_{filename}"
	return f"{filename}"

class Slide(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	custom_name = models.CharField(max_length=250, blank=True, null=True)
	index = models.PositiveIntegerField(default=1)
	image = models.ImageField(upload_to=slide_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)
	tag = models.ManyToManyField(Tag)
	category = models.ManyToManyField(Category)

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		if not self.custom_name:
			timestamp = timezone.now().strftime("%Y%m%d")
			self.custom_name = f"{timestamp}"
		super().save(*args, **kwargs)

def banner_upload_path(instance, filename):
	banner_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{banner_name}_{filename}"
	return f"{filename}"

class Banner(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	custom_name = models.CharField(max_length=250, blank=True, null=True)
	index = models.PositiveIntegerField(default=1)
	image = models.ImageField(upload_to=banner_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)
	tag = models.ManyToManyField(Tag)
	category = models.ManyToManyField(Category)
	size = models.CharField(max_length=250, default='small')
	
	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		if not self.custom_name:
			timestamp = timezone.now().strftime("%Y%m%d")
			self.custom_name = f"{timestamp}"
		super().save(*args, **kwargs)
	
class Faq(models.Model):
	question = models.CharField(max_length= 500)
	answer = models.CharField(max_length=2000)

class WithdrawRecord(models.Model):
	sheba = models.CharField(max_length = 250)
	amount = models.IntegerField()
	created_date = models.DateTimeField(auto_now_add=True)
	is_paid = models.BooleanField(default=False)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

	def __str__(self):
		return f'{self.amount} - {self.shamsi_created_date}'

class BlogCategory(models.Model):
	name = models.CharField(max_length=250)

	def get_slug(self):
		return self.name.replace('/','').replace(' ','-')

	def __str__(self):
		return self.name

class BlogPost(models.Model):
	title = models.CharField(max_length=250)
	slug = models.CharField(max_length = 250)
	category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, null=True, blank=True)
	body = RichTextField(default = "insert the post body")
	created_date = models.DateTimeField(auto_now_add=True)
	published = models.BooleanField(default=False)
	meta_description = models.CharField(max_length=500, default='')
	meta_keywords = models.CharField(max_length=500, default='')
	meta_og_title = models.CharField(max_length=250, default= '')
	meta_og_description = models.CharField(max_length=1000, default= '')
	meta_tc_title = models.CharField(max_length=250, default= '')
	meta_tc_description = models.CharField(max_length=250, default= '')

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

def thumbnail_upload_path(instance, filename):
	thumbnail_name = instance.alt_name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{thumbnail_name}_{filename}"
	return f"{filename}"

class PostThumbnail(models.Model):
	post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	custom_name = models.CharField(max_length=250, blank=True, null=True)
	image = models.ImageField(upload_to=thumbnail_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created',)

	def save(self, *args, **kwargs):
		if not self.custom_name:
			self.custom_name = f"{self.post.title}"
		super().save(*args, **kwargs)

class UploadedImages(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	image = models.ImageField()

def category_upload_path(instance, filename):
	category_name = instance.alt_name.replace(" ", "_")
	filename = f"{category_name}_{filename}"
	return f"{filename}"

class CategoryImage(models.Model):
	alt_name = models.CharField(max_length=250, null=True, blank=True)
	image = models.ImageField(upload_to=category_upload_path, default='media/11.png')
	created = models.DateTimeField(auto_now_add=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)

	class Meta:
		ordering = ('created',)

	def get_absolute_url(self):
		return self.image.url

	def save(self, *args, **kwargs):
		if not self.alt_name:
			self.custom_name = f"{self.category.name}"
		super().save(*args, **kwargs)

class FeaturedCategories(models.Model):
	categories = models.ManyToManyField(Category, blank=True)

class Subscription(models.Model):
	email=models.EmailField()

class Services(models.Model):
	delivery = models.CharField(max_length=250, default = 'شیوه‌های ارسال متنوع قابل انتخاب توسط شما')
	originality = models.CharField(max_length=250, default = 'تحویل کالای اصل بدون کوچکترین مغایرت با توضیحات')
	payments = models.CharField(max_length=250, default = 'درگاه پرداخت امن با پشتیبانی از تمامی کارت‌های بانکی')

def brand_upload_path(instance):
	logo_name = instance.name.replace(" ", "_")
	timestamp = timezone.now().strftime("%Y%m%d")
	filename = f"{logo_name}"
	return f"{filename}"

class Brand(models.Model):
	name = models.CharField(max_length=250)
	logo = models.ImageField(upload_to=brand_upload_path,null=True ,blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		# بررسی اگر نام برند تغییر کرده باشد
		if self.pk:
			original_name = Brand.objects.get(pk=self.pk).name
			if original_name != self.name:
				# بروزرسانی نام برند در محصولات مرتبط
				Product.objects.filter(brand=original_name).update(brand=self.name)
		super().save(*args, **kwargs)

class Recommender(models.Model):
	full_name = models.CharField(max_length = 250)
	phone_number = models.CharField(max_length = 250)
	created_date = models.DateTimeField(auto_now_add = True)
	balance = models.IntegerField(default = 0)
	referal_code = models.CharField(max_length = 6)

class Ticket(models.Model):
	subject = models.CharField(max_length=250)
	body = models.TextField()
	is_answered = models.BooleanField(default=False)
	is_closed = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

	def get_reply_date(self):
		reply = TicketReply.objects.filter(ticket = self).first()
		if reply != None:
			return JalaliDatetime(reply.created_date).strftime('%Y/%m/%d')
		return 'بدون پاسخ'

	def __str__(self):
		return f'{self.subject}'

class TicketReply(models.Model):
	body = models.CharField(max_length=1000)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
	created_date = models.DateTimeField(auto_now_add=True)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

class Domain(models.Model):
	domain = models.CharField(max_length=100)
	is_active = models.BooleanField(default=False)
	created_date = models.DateTimeField(auto_now_add=True)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created_date).strftime('%Y/%m/%d')

class Filter(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	name = models.CharField(max_length=250)

	def get_values(self):
		return FilterValue.objects.filter(filter=self)

	def __str__(self):
		return f'{self.name}'
	
class FilterValue(models.Model):
	value = models.CharField(max_length=250)	
	product = models.ForeignKey('Product',on_delete=models.CASCADE, related_name='filter_values', null=True, blank=True)  # اضافه کردن related_name
	filter = models.ForeignKey(Filter, on_delete=models.CASCADE, null=True, blank=True)

class ProductFilter(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
	values = models.ManyToManyField(FilterValue, blank=True)

	def __str__(self):
		return f"{self.product.name} - {self.filter.name}"
	
class Announcement(models.Model):
	subject = models.CharField(max_length=250, blank = True, null=True)
	message = models.TextField()
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)

	@property
	def shamsi_created_date(self):
		return JalaliDatetime(self.created).strftime('%Y/%m/%d')

class ExpressDeliveryInterval(models.Model):
	start_time = models.IntegerField()
	end_time = models.IntegerField()
	total_cap = models.IntegerField(default=100)
	teken_cap = models.IntegerField(default=0)