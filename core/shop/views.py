from django.shortcuts import render, redirect, get_object_or_404
from random import randint
from django.core.files.base import ContentFile
from django import forms
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import re, os
import requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from .utils import IsOwnerUserMixin, IsCustomerUserMixin
from django.http import HttpResponse, JsonResponse
import pytz
from django.views.generic import  DeleteView
from .forms import *
from django.views import View
from shop.models import *
import random
from accounts.models import User
from utils import send_otp_code
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from django.apps import apps
from datetime import datetime
from khayyam import JalaliDatetime
from django.db.models import Q
from googletrans import Translator
import re



MERCHANT = Store.objects.all().first().merchant
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
# CallbackURL = 'http://127.0.0.1:8000/shop//orders/verify/'

store_name = Store.objects.all().first().name
store = Store.objects.all().first()
current_app_name = apps.get_containing_app_config(__name__).name


class IndexView(View):

	def get(self, request):
		current_page = request.path
		slides = Slide.objects.all()
		small_banners = Banner.objects.filter(size='small')
		big_banners = Banner.objects.filter(size='big')
		posts = BlogPost.objects.all()
		services = Services.objects.all().first()
		products = Product.objects.all()
		to_products = f'{current_app_name}:product_detail'
		featured_categories = FeaturedCategories.objects.all().first()
		most_viewed_products = Product.objects.order_by('-views')[:8]
		return render(request, f'{current_app_name}/index_{store.template_index}.html', {'services':services,
																				   'posts':posts,
																				   'featured_categories':featured_categories,
																				   'to_products':to_products ,
																				   'products':products ,
																				   'store_name':store_name, 
																				   'slides':slides, 
																				   'small_banners':small_banners, 
																				   'big_banners':big_banners,
																				   'most_viewed_products':most_viewed_products})

class OwnerView(View):

	form_class = OwnerForm
	template_name = 'shop/owner.html'

	def get(self, request):
		form = self.form_class()
		return render(request, self.template_name, {'form':form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		store = Store.objects.get(name=store_name)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			if len(phone_number) != 11:
				return render(request, self.template_name, {'message':'شماره تماس صحیح نیست'})

			# 2. بررسی شروع با '09'
			if not phone_number.startswith('09'):
				return render(request, self.template_name, {'message':'شماره تماس صحیح نیست'})
			full_name = form.cleaned_data['full_name']
			owner = Owner.objects.filter(phone_number=phone_number).first()
			if owner != None:
				previous_codes = OtpCode.objects.filter(phone_number = phone_number)
				previous_codes.delete()
				random_code = random.randint(100000,999999)
				send_otp_code(phone_number,random_code)
				new_otp = OtpCode.objects.create(phone_number = phone_number, code = random_code) 
				return redirect('shop:verify-owner', phone_number)
			
			owner = Owner.objects.create(phone_number = phone_number,full_name=full_name)
			user, create = User.objects.get_or_create(phone_number = phone_number)
			user.full_name= full_name
			user.save()
			previous_codes = OtpCode.objects.filter(phone_number = phone_number)
			previous_codes.delete()
			random_code = random.randint(100000,999999)
			send_otp_code(phone_number,random_code)
			new_otp = OtpCode.objects.create(phone_number = phone_number, code = random_code) 
			return redirect('shop:verify-owner', phone_number=phone_number)
		message = 'ورودی نا معتبر'
		return render(request, self.template_name, {'message':message, 'form':form})

class VerifyOwnerView(View):
	form_class = VerifyOwnerForm
	template_name = f'{current_app_name}/verify_owner.html'

	def get(self, request, phone_number):
		form = self.form_class()
		return render(request, self.template_name, {'form':form})
	
	def post(self, request, phone_number, *args, **kwargs):
		form = AuthenticationCodeForm(request.POST)
		if form.is_valid():
			owner_phone = phone_number
			owner = Owner.objects.filter(phone_number = owner_phone).first()
			user = User.objects.filter(phone_number = owner_phone).first()
			customer = Customer.objects.get_or_create(phone_number=phone_number)
			request.user = user
			last_sent_otp = OtpCode.objects.filter(phone_number = owner_phone).first()
			recieved_code = form.cleaned_data['code']
			if last_sent_otp.code == recieved_code:
				user.is_shopowner = True
				owner.save()
				user.save()
				login(request, user)
				if user.is_verified == True:
					return redirect(f'{current_app_name}:owner_dashboard')
				return redirect(f'{current_app_name}:owner_dashboard_tutorials')
			return render(request, self.template_name, {'form':form, 'message':'کد تایید اشتباه است.'})
		return render(request, self.template_name, {'form':form, 'message':'ورودی نامعتبر'})
	
class AnswerMessageView(IsOwnerUserMixin, View):

	def get(self, request, message_id, status_id, *args, **kwargs):
		store = Store.objects.get(name=store_name)
		message = ContactMessage.objects.get(id=message_id)
		if status_id == 1:
			message.is_answered = True
			message.save()
		else:
			message.is_answered = False
			message.save()
		
		return redirect(f'{current_app_name}:owner_dashboard_messages')

class CustomerDashboardView(View):

	def get(self, request, *args, **kwargs):
		if isinstance(request.user, AnonymousUser):
			return redirect(f'{current_app_name}:customer_authentication')
		customer = Customer.objects.get(phone_number = request.user.phone_number)
		orders = Order.objects.filter(customer=customer)
		num_of_orders = orders.count()
		paid_status = OrderStatus.objects.get(id=1)
		total = 0
		for order in orders:
			if order.status == paid_status:
				total = total + order.total_price
		favorites = customer.favorites.all()
		number_of_favs = favorites.count()
		return render(request, f'{current_app_name}/customer-dashboard_{store.template_index}.html', {
			'customer':customer,
			'orders':orders,
			'num_of_orders':num_of_orders,
			'total':total,
			'store_name':store_name,
			'store':store,
			'number_of_favs':number_of_favs,
		})

class CustomerDashboardOrdersView(IsCustomerUserMixin, View):

	def get(self, request):
		customer = Customer.objects.get(phone_number=request.user.phone_number)		
		paid_status = OrderStatus.objects.get(id=1)
		paid_orders = Order.objects.filter(customer=customer, status=paid_status)
		number_paid_orders = paid_orders.count()
		orders = Order.objects.filter(customer = customer)

		return render(request, f'{current_app_name}/customer-dashboard-orders_{store.template_index}.html', 
				{'store_name':store_name,
				'number_of_paid_orders':number_paid_orders,
				'paid_orders':paid_orders,
				'customer':customer,
				'orders':orders})

class CustomerDashboardOrderDatailView(IsCustomerUserMixin, View):
	
	def get(self, request, order_id):
		order = get_object_or_404(Order, id=order_id)
		return render(request, f'{current_app_name}/order-detail-customer_{store.template_index}.html',
				 {'order':order, 'store_name':store_name})

class CustomerDashboardFavoritesView(IsCustomerUserMixin, View):

	def get(self, request):
		customer = Customer.objects.get(phone_number=request.user.phone_number)
		products = customer.favorites.all()
		to_products = f'{current_app_name}:product_detail'
	

		return render(request, f'{current_app_name}/customer-dashboard-favorites_{store.template_index}.html',
				 {'store_name':store_name,
				'products':products,
				'to_products':to_products,
				'customer':customer,
				})

class CustomerDashboardInfoView(IsCustomerUserMixin, View):

	form_class = CustomerForm
	def get(self, request):
		customer = Customer.objects.get(phone_number=request.user.phone_number)
		form = CustomerForm
		return render(request, f'{current_app_name}/customer-dashboard-info_{store.template_index}.html', 
				{'form': form, 'customer':customer})

	def post(self, request):
		customer = Customer.objects.get(phone_number=request.user.phone_number)
		form = self.form_class(request.POST)
		if form.is_valid():
			customer.full_name = form.cleaned_data['full_name']
			customer.email = form.cleaned_data['email']
			customer.city = form.cleaned_data['city']
			customer.zip_code = form.cleaned_data['zip_code']
			customer.address = form.cleaned_data['address']
			customer.save()
			return redirect(f'{current_app_name}:customer_dashboard_info')

class CustomerDashboardCommentsView(IsCustomerUserMixin, View):

	def get(self, request):
		store = get_object_or_404(Store, name=store_name)
		customer = Customer.objects.get(phone_number=request.user.phone_number)
		comments = Comment.objects.filter(sender=customer)
		return render(request, f'{current_app_name}/customer-dashboard-comments_{store.template_index}.html',
				 {'comments': comments, 'customer':customer})

class DeliveryListCreateView(IsOwnerUserMixin ,View):

	template_name = f'{current_app_name}/owner-dashboard-delivery.html'

	def get(self, request, *args, **kwargs):
		form = DeliveryForm
		store = Store.objects.get(name=store_name)
		delivery_methods = Delivery.objects.all()
		create_delivery_url = f'{current_app_name}:owner_dashboard_delivery'
		edit_delivery_url = f'{current_app_name}:edit_delivery'
		return render(request, self.template_name, {'edit_delivery_url':edit_delivery_url,
													'create_delivery_url':create_delivery_url,
													'form': form, 
													'delivery_methods':delivery_methods,
													'store_name':store_name})

	def post(self, request, *args, **kwargs):
		form = DeliveryForm(request.POST)
		if form.is_valid():
			store = Store.objects.get(name=store_name)
			delivery = Delivery.objects.create(
				
				name = form.cleaned_data['name'],
				price = form.cleaned_data['price'],
			)
			delivery_methods = Delivery.objects.all()
			create_delivery_url = f'{current_app_name}:delivery-list-and-create'
			edit_delivery_url = f'{current_app_name}:edit_delivery'
			return redirect(f'{current_app_name}:owner_dashboard_delivery')
		create_delivery_url = f'{current_app_name}:delivery-list-and-create'
		edit_delivery_url = f'{current_app_name}:edit_delivery'
		return render(request, self.template_name, {'edit_delivery_url':edit_delivery_url,
													'create_delivery_url':create_delivery_url,
													'form': form, 
													'delivery_methods':delivery_methods,
													'store_name':store_name})

class DeliveryEditView(IsOwnerUserMixin ,View):

	def post(self, request, pk, *args, **kwargs):
		delivery = get_object_or_404(Delivery, pk=pk)
		form = DeliveryForm(request.POST)
		if form.is_valid():
			delivery.price = form.cleaned_data['price']
			delivery.save()
			return redirect('shop:owner_dashboard_delivery') 
		store = Store.objects.filter(name = store_name).first()
		delivery_methods = Delivery.objects.all()
		create_delivery_url = f'{current_app_name}:delivery-list-and-create'
		edit_delivery_url = f'{current_app_name}:edit_delivery'
		return render(request, self.template_name, {'edit_delivery_url':edit_delivery_url,
													'create_delivery_url':create_delivery_url,
													'form': form, 
													'delivery_methods':delivery_methods,
													'store_name':store_name})

class DeliveryDeleteView(IsOwnerUserMixin, View):
		
	def get(self, request, pk, *args, **kwargs):
		delivery = Delivery.objects.get(pk=pk)
		delivery.delete()
		return redirect(f'{current_app_name}:owner_dashboard_delivery')

class CategoryCreateView(IsOwnerUserMixin, View):

	def post(self, request):
		form = CategoryForm(request.POST)
		if form.is_valid():
			store = Store.objects.get(name=store_name)
			name = form.cleaned_data['name']
			parent_id = form.cleaned_data['parent']
			is_sub = form.cleaned_data['is_sub']
			# translator = Translator()
			# translation = translator.translate(name)
			# slug = re.sub(r'\s+', '-', translation.text)
			# slug = slug.lower()
			slug = name.lower().replace(' ','-')
			category = Category.objects.create(
											   name=name,
											   is_sub=is_sub,
											   slug=slug)
			if parent_id != []:
				parent = Category.objects.filter(id=int(parent_id[0])).first()
				if parent != None:
					category.parent = parent
					category.save()

			return redirect(f'{current_app_name}:owner_dashboard_categories') 	 
		return render(request, f'{current_app_name}/category_list.html', {'form': form})
	
class CategoryListView(IsOwnerUserMixin, View):

	template_name = 'shop/owner-dashboard-categories.html'

	def get(self, request):
		store = Store.objects.get(name=store_name)
		categories = Category.objects.all()
		create_category_url = f'{current_app_name}:create_category'
		edit_category_url = f'{current_app_name}:edit_category'
		return render(request, self.template_name, {'create_category_url':create_category_url,
											  		'edit_category_url':edit_category_url,
													'categories':categories,
													'store_name':store_name})

class CategoryDetailView(IsOwnerUserMixin, View):

	template_name = 'shop/category_detail.html'

	def get(self, request, pk):
		store = Store.objects.get(name=store_name)
		category = Category.objects.get( pk=pk)

		return render(request, self.template_name, {'category':category})
	
class CategoryUpdateView(IsOwnerUserMixin, View):

	template_name = 'shop/editcategory.html'

	def get(self, request, pk):
		store = Store.objects.get(name = store_name)
		categories = Category.objects.all()
		category = Category.objects.get(id=pk)

		return render(request, self.template_name, {'category':category, 'categories':categories})

	def post(self, request, pk, *args, **kwargs):
		category = Category.objects.filter(id=pk).first()
		form = CategoryForm(request.POST)
		if form.is_valid():
			category = Category.objects.get(id = pk)
			category.store = Store.objects.get(name=store_name)
			category.name = form.cleaned_data['name']
			parent_id = form.cleaned_data['parent']
			if parent_id != '0':
				category.parent = Category.objects.get(id=parent_id)
				category.is_sub = True
			slug = category.name.lower().replace(' ','-')
			category.slug = slug
			if parent_id != []:
				parent = Category.objects.filter(id=int(parent_id[0])).first()
				if parent != None:
					category.parent = parent
			category.save()
			return redirect('shop:owner_dashboard_categories') 	 
		return render(request, self.template_name, {'form': form})

class CategoryDeleteView(IsOwnerUserMixin, DeleteView):

	def get(self, request, pk, *args, **kwargs):
		category = Category.objects.get(pk=pk)
		category.delete()
		return redirect(f'{current_app_name}:owner_dashboard_categories') 

class UploadProductImagesView(IsOwnerUserMixin, View):

	form_class = ProductImageForm
	template_name = f'{current_app_name}/editproduct.html'

	def post(self, request, pk, *args, **kwargs):
		product = Product.objects.get(pk=pk)
		form = ProductImageForm(request.POST, request.FILES)
		images = ProductImage.objects.filter(product=product)
		if form.is_valid():
			alt_name = form.cleaned_data['alt_name']
			print(form.cleaned_data)
			if alt_name == None:
				alt_name = f'{product.name}'
			images = request.FILES.getlist('images')
			store = Store.objects.get(name=store_name)
			for image in images:
				ProductImage.objects.create(alt_name=alt_name, image=image, product=product)
				new_upload = UploadedImages.objects.create(
				
				image = image,
				alt_name = alt_name,
			)
			return redirect(f'{current_app_name}:product_update', product.id)
		return render(request, self.template_name, {'images':images, 'form': form, 'product':product, 'store_name':store_name})

class DeleteProductImageView(IsOwnerUserMixin, View):

	def get(self, request, product_id, image_id):
		product = Product.objects.get(id=product_id)
		image = ProductImage.objects.get(id = image_id)
		image.delete()		
		return redirect(f'{current_app_name}:product_update', product.id)

class CopyProductView(IsOwnerUserMixin, View):

	def get(self, request, product_id):
		store = Store.objects.get(name = store_name)
		product = Product.objects.get(id = product_id)
		new_product = Product.objects.create(
			name = product.name + 'copy',
			
			slug = product.slug + str(randint(999, 10000)),
			price = product.price,
			description = product.description,
			brand = product.brand,
			sales_price = product.sales_price,
			off_active = product.off_active,
			available = product.available, 
			features = product.features,
		)
		default_variety = Variety.objects.create(
				
				name = 'default variety',
				product = new_product, 
				stock = 2,
			)

		for category in product.category.all():
			new_product.category.add(category)
		for tag in product.tags.all():
			new_product.tags.add(tag)
		product.save()

		return redirect(f'{current_app_name}:owner_dashboard_products')

class ProductCreateView(IsOwnerUserMixin, View):

	template_name = f'{current_app_name}/addproduct.html'

	def get(self, request):
		store = Store.objects.get(name=store_name)
		form = ProductForm
		categories = Category.objects.all()
		product_update_url = f'{current_app_name}:product_update'
		add_variety_url = f'{current_app_name}:add_variety'
		update_variety_url = f'{current_app_name}:update_variety'
		image_delete_url = f'{current_app_name}:product_image_delete'
		delete_variety_url = f'{current_app_name}:delete_variety'
		return render(request, self.template_name, {'form': form, 
													'categories': categories, 
													'store_name':store_name, 
													'product_update_url':product_update_url,
													'add_variety_url':add_variety_url,
													'update_variety_url':update_variety_url,
													'image_delete_url':image_delete_url,
													'delete_variety_url':delete_variety_url})

	def post(self, request):
		form = ProductForm(request.POST)
		store = Store.objects.get(name = store_name)
		categories = Category.objects.all()
		if form.is_valid():
			store = Store.objects.get(name=store_name)
			print(form.cleaned_data)
			name = form.cleaned_data['name']
			if not name:
				return render(request, self.template_name, {'form': form, 'categories':categories, 'name_message':'لطفا نام محصول را وارد نمایید.'})
			slug = name.lower().replace(' ','-')
			price = form.cleaned_data['price']
			if not price:
				price = 0
			description = form.cleaned_data['description']
			tags = form.cleaned_data['tags']
			brand = form.cleaned_data['brand']
			processed_tags = [line for line in tags.splitlines()]
			new_brand, create = Brand.objects.get_or_create( name=brand)			
			sales_price = form.cleaned_data['sales_price']
			sales_price = sales_price
			off_active = form.cleaned_data['off_active']
			if off_active == ['1']:
				off_active = True
			if off_active == ['0']:
				off_active = False
			features = form.cleaned_data['features'].replace('\r\n', '<br>')

			product = Product.objects.create(
											 name = name,
											 slug = slug,
											 price = price, 
											 brand = brand,
											 description = description,
											 sales_price =sales_price,
											 off_active = off_active, 
											 features = features,
											 )
			category = form.cleaned_data['category']
				
			for cat in category:
				if cat == '0':
					product_cat, create = Category.objects.get_or_create(name='دسته‌بندی نشده', is_sub=False,slug='uncategorized')
				else:
					product_cat = Category.objects.get(id = int(cat))
				product.category.add(product_cat)

			product.tags.clear()

			for tag in processed_tags:
				name = tag
				slug = tag.replace(' ','-')
				new_tag, create = Tag.objects.get_or_create(name=name, slug=slug)
				product.tags.add(new_tag)
			
			product.save()

			default_variety = Variety.objects.create(
				
				name = 'default variety',
				product = product, 
				stock = 2,
			)

			return redirect(f'{current_app_name}:product_update', product.id)
		return render(request, self.template_name, {'form': form, 'categories':categories})
	
class ProductMetaTagsUpdateView(IsOwnerUserMixin, View):

	def post(self, request, product_slug):
		form = MetaForm(request.POST)
		if form.is_valid():
			store = Store.objects.get(name = store_name)
			product = Product.objects.get(slug = product_slug)
			product.meta_description = form.cleaned_data['meta_description']
			product.meta_keywords = form.cleaned_data['meta_keywords']
			product.meta_og_title = form.cleaned_data['meta_og_title']
			product.meta_og_description = form.cleaned_data['meta_og_description']
			product.meta_tc_title = form.cleaned_data['meta_tc_title']
			product.meta_tc_description = form.cleaned_data['meta_tc_description']
			product.save()
			return redirect(f'{current_app_name}:product_update', product.id)

class ProductUpdateView(IsOwnerUserMixin, View):

	template_name = f'{current_app_name}/editproduct.html'

	def get(self, request, product_id):
		store = Store.objects.get(name=store_name)
		product = Product.objects.get(id=product_id)
		form = ProductForm
		form2 = ProductImageForm
		form3 = MetaForm
		form4 = VarietyForm
		form5 = VarietyUpdateForm
		categories = Category.objects.all()
		images = ProductImage.objects.filter(product=product)
		varieties = Variety.objects.filter(product=product)
		filters = Filter.objects.all()
		filter_values = FilterValue.objects.filter(product = product)
		upload_img_url = f'{current_app_name}:product_image_upload'
		product_update_url = f'{current_app_name}:product_update'
		add_variety_url = f'{current_app_name}:add_variety'
		update_variety_url = f'{current_app_name}:update_variety'
		image_delete_url = f'{current_app_name}:product_image_delete'
		delete_variety_url = f'{current_app_name}:delete_variety'
		colors = ProductColor.objects.all()
		return render(request, self.template_name, {'form': form,
											  		'colors': colors, 
													'categories': categories, 
													'store_name':store_name, 
													'product': product, 
													'images':images, 
													'varieties':varieties,
													'form2':form2,
													'form3':form3,
													'form4':form4,
													'form5':form5,
													'filter_values':filter_values,
													'upload_img_url':upload_img_url,
													'product_update_url':product_update_url,
													'add_variety_url':add_variety_url,
													'update_variety_url':update_variety_url,
													'image_delete_url':image_delete_url,
													'delete_variety_url':delete_variety_url,
													'filters':filters})

	def post(self, request, product_id, *args, **kwargs):
		store = Store.objects.get(name=store_name)
		product = Product.objects.get(id = product_id)
		form = ProductForm(request.POST)
		categories = Category.objects.all()
		if form.is_valid():
			print('QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ')
			print(form.cleaned_data)
			color_codes = request.POST.getlist('color')
			print(color_codes)
			if color_codes != []:
				for code in color_codes:
					new_color = ProductColor.objects.get(id = int(code))
					product.color.add(new_color)
			name = form.cleaned_data['name']
			product.name = name
			price = form.cleaned_data['price']
			product.price = price
			sales_price = form.cleaned_data['sales_price']
			product.sales_price = sales_price
			off_active = form.cleaned_data['off_active']
			if off_active == '1':
				product.off_active = True
			if off_active == '0':
				product.off_active = False
			original = form.cleaned_data['is_original']
			if original == '0':
				product.is_original = False
			if original == '1':
				product.is_original = True
			brand = form.cleaned_data['brand']
			new_brand, create = Brand.objects.get_or_create(name=brand)
			product.brand = brand
			category = form.cleaned_data['category']
			if category != None:
				product.category.clear()
				product.save()
				if category == '0':
					product_cat, create = Category.objects.get_or_create(name='دسته‌بندی نشده', is_sub=False,slug='uncategorized')
				else:
					product_cat = Category.objects.get(id = int(category))
				product.category.add(product_cat)
				product.save()
			description = form.cleaned_data['description']
			product.description = description
			features = form.cleaned_data['features']
			product.features = features.replace('\r\n', '<br>')
			tags = form.cleaned_data['tags']
			processed_tags = [line for line in tags.splitlines()]
			product.tags.clear()

			for tag in processed_tags:
				name = tag
				slug = tag.replace(' ','-')
				new_tag, create = Tag.objects.get_or_create(name=name, slug=slug)
				product.tags.add(new_tag)
			
			product.save()
			
			return redirect(f'{current_app_name}:product_update', product.id)
		else:
			categories = Category.objects.all()
			images = ProductImage.objects.filter(product=product)
			varieties = Variety.objects.filter(product=product)
			form = ProductForm
			form2 = ProductImageForm
			form3 = MetaForm
			form4 = VarietyForm
			form5 = VarietyUpdateForm
			upload_img_url = f'{current_app_name}:product_image_upload'
			product_update_url = f'{current_app_name}:product_update'
			add_variety_url = f'{current_app_name}:add_variety'
			update_variety_url = f'{current_app_name}:update_variety'
			image_delete_url = f'{current_app_name}:product_image_delete'
			delete_variety_url = f'{current_app_name}:delete_variety'
			return render(request, self.template_name, {'form': form, 
														'categories': categories, 
														'store_name':store_name, 
														'product': product, 
														'images':images, 
														'form2':form2,
														'form3':form3,
														'form4':form4,
														'form5':form5,
														'varieties':varieties,
														'upload_img_url':upload_img_url,
														'product_update_url':product_update_url,
														'add_variety_url':add_variety_url,
														'update_variety_url':update_variety_url,
														'image_delete_url':image_delete_url,
														'delete_variety_url':delete_variety_url})

class ProductListView(View):

	def get(self, request):
		items_per_page = 12
		store = Store.objects.get(name=store_name)
		categories = Category.objects.all()
		products = Product.objects.filter(verified = True)
		paginator = Paginator(products, items_per_page)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		brands = Brand.objects.all()
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		colors = ProductColor.objects.all()
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				{'products': products, 
	 			'colors': colors,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'brands':brands,
				'sizes':sizes,
				'price_ranges':price_ranges})
	
	def post(self, request, *args, **kwargs):
		main_filters = {}
		filters = []
		product_cat = None
		price_range = None
		selected_brand = None
		form = FilterProductsForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			store = Store.objects.get(name=store_name)
			category = form.cleaned_data['category']
			products = set()
			if category != '':
				product_cat = Category.objects.filter(id = int(category)).first()
				if category != '0':
					cat_products = Product.objects.filter(category=product_cat)
					for product in cat_products:
						products.add(product)
					if product_cat.get_sub_categories() != None:
						sub_categories = product_cat.get_sub_categories()
						for sub_cat in sub_categories:
							sub_products = sub_cat.product_set.all()
							for product in sub_products:
								products.add(product)


				else:
					products = Product.objects.all()
				categories = []
				if product_cat:
					if product_cat.is_sub == True:
						categories = []
					else:
						categories = [cat for cat in Category.objects.all() if cat.parent == product_cat]
			product_ids = [product.id for product in products]
			products = Product.objects.filter(id__in=product_ids)

			brands = Brand.objects.all()	
			brand = form.cleaned_data['brand']
			if brand != '':
				selected_brand = Brand.objects.filter(id = brand).first()
				if brand != '0':
					products = products.filter(brand = selected_brand.name)
					main_selected_brand = Brand.objects.filter(id = brand).first()
					brands = list(Brand.objects.filter(id = brand))
				else:
					products = products.all()
					if category != '0':
						brands = product_cat.get_category_brands()
							
			filtered_products = []
			price_ranges = form.cleaned_data['price_range']
			if price_ranges != '0':
				for price in price_ranges:
					selected_price_range = PriceRange.objects.filter(id = int(form.cleaned_data['price_range'])).first()
			else:
				selected_price_range = None
			if selected_price_range != None:
				for product in products:
								if product.price<selected_price_range.max_value and product.price>=selected_price_range.min_value:
									filtered_products.append(product.id)
			if filtered_products != []:
				products = products.filter(id__in=filtered_products)
			if selected_price_range != None and filtered_products == []:
				products = []

			filtered_products = []
			color = form.cleaned_data['color']
			if color != '0' and color != '':
				selected_color = ProductColor.objects.filter(id = int(form.cleaned_data['color'])).first()
			else:
				selected_color = None
			if selected_color != None:
				for product in products:
					if selected_color in product.color.all():
						filtered_products.append(product.id)
			if filtered_products != []:
				products = products.filter(id__in=filtered_products)
			if selected_color != None and filtered_products == []:
				products = []
			
			store = Store.objects.get(name=store_name)
			products_urls = f'{current_app_name}:product_detail'
			sizes = Size.objects.all()
			price_ranges = PriceRange.objects.all()

			my_forms = []
			if category != '0':
				selected_category = Category.objects.filter(id = int(category)).first()
				filters = Filter.objects.all()
				for filter in filters:
					values = filter.value.all()
					class FeatureFilterForm(forms.Form):
						name = filter.name
						choices = tuple([(value.value, value.value) for value in values])
						فیلترها = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
					new_form = FeatureFilterForm
					my_forms.append(new_form)
				category = Category.objects.get(slug = selected_category.slug)
				filters = Filter.objects.filter(category=category)
			else:
				selected_category = None

			selected_values = []
			active_filters = []
			for key, value in request.session.items():
				if key.startswith('filter-'):
					
					filter_name = key.replace('filter-', '')
					selected_filter = Filter.objects.get( name = filter_name)
					for posi_value in selected_filter.value.all():
						if posi_value.value in value:
							new_active_filter = {'filter':selected_filter,'value':posi_value}
							active_filters.append(new_active_filter)
							selected_values.append(posi_value.id)

			paginator = Paginator(products, 12)
			page = request.GET.get('page', 1)
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				# اگر شماره صفحه یک عدد نیست
				products = paginator.page(1)
			except EmptyPage:
				# اگر شماره صفحه بیشتر از تعداد کل صفحات است
				products = paginator.page(paginator.num_pages)

			colors = ProductColor.objects.all()

			return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				 {'products': products, 
	  			'colors': colors,
				'brands':brands,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges,
				'selected_brand':selected_brand,
				'selected_price_range':selected_price_range,
				'selected_category':selected_category,
				'filters':filters,
				'category':selected_category,
				'my_forms':my_forms,
				'active_filters':active_filters,
				'main_filters': main_filters,
				'main_selected_category' : product_cat,
				'main_selected_brand' : selected_brand,
				'main_selected_price_range' : selected_price_range})
					
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', {'store_name':store_name})

class FilterTagProducts(View):

	def get(self, request, tag_slug):
		items_per_page = 12
		store = Store.objects.get(name=store_name)
		categories = Category.objects.all()
		products = Product.objects.filter( tags__slug=tag_slug)
		paginator = Paginator(products, items_per_page)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		brands = Brand.objects.all()
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				{'products': products, 
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'brands':brands,
				'sizes':sizes,
				'price_ranges':price_ranges})

class FeaturedProductListView(View):

	def get(self, request, featured_products_id):
		products = set()
		slide = Slide.objects.get(id = featured_products_id)
		if slide.tag:
			for tag in slide.tag.all():
				for product in tag.get_products():  # پیمایش کوئری‌ست
					products.add(product)
		if slide.category:
			for category in slide.category.all():
				for product in category.get_products():  # پیمایش کوئری‌ست
					products.add(product)
		products = list(products)
		categories = Category.objects.all()
		# products = products.filter(verified = True)
		paginator = Paginator(products, 12)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		items_per_page = 12
		paginator = Paginator(products, items_per_page)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		brands = Brand.objects.all()
		colors = ProductColor.objects.all() 		
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html',
				 {'products': products, 
	  			'brands': brands,
				'colors': colors,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges})
	
class SpecialProductsListView(View):

	def get(self, request, featured_products_id):
		products = set()
		banner = Banner.objects.get(id = featured_products_id)
		if banner.tag:
			for tag in banner.tag.all():
				for product in tag.get_products():  # پیمایش کوئری‌ست
					products.add(product)
		if banner.category:
			for category in banner.category.all():
				for product in category.get_products():  # پیمایش کوئری‌ست
					products.add(product)
		products = list(products)
		categories = Category.objects.all()
		# products = products.filter(verified = True)
		paginator = Paginator(products, 12)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		items_per_page = 12
		paginator = Paginator(products, items_per_page)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		brands = Brand.objects.all()
		colors = ProductColor.objects.all() 		
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html',
				 {'products': products, 
	  			'brands': brands,
				'colors': colors,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges})

class AddToFavoritesView(View):

	def get(self, request, product_id, ref, *args, **kwargs):
		if isinstance(request.user, AnonymousUser):
			return redirect(f'{current_app_name}:customer_authentication')
		store = Store.objects.get(name=store_name)
		product = Product.objects.get(id=product_id)
		phone = request.user.phone_number
		customer = Customer.objects.filter(phone_number=phone).first()
		if product in customer.favorites.all():
			customer.favorites.remove(product)
		else:
			customer.favorites.add(product)

		if ref == 'index':
			return redirect(f'{current_app_name}:index')
		if ref == 'products':
			return redirect(f'{current_app_name}:product_list')
		if ref == 'product_detail':
			return redirect(f'{current_app_name}:product_detail', product.slug)

		if ref == 'fav_list':
			return redirect(f'{current_app_name}:customer_dashboard_favorites')			

class CategoryProductsListView(View):

	def get(self, request, category_slug, *args, **kwargs):
		store = Store.objects.get(name = store_name)
		filters = Filter.objects.all()
		my_forms = []
		for filter in filters:
			values = filter.value.all()
			class FeatureFilterForm(forms.Form):
				name = filter.name
				choices = tuple([(value.value, value.value) for value in values])
				فیلترها = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
			new_form = FeatureFilterForm
			my_forms.append(new_form)
		category = Category.objects.get(slug = category_slug)
		categories = []
		if category.is_sub == True:
			categories = []
		else:
			categories = [cat for cat in Category.objects.all() if cat.parent == category]
		filters = Filter.objects.filter(category=category)
		products = set()
		cat_products = [product for product in Product.objects.filter(category=category) if product.verified == True]
		for product in cat_products:
			products.add(product)
		if category.get_sub_categories() != None:
			sub_categories = category.get_sub_categories()
			for sub_cat in sub_categories:
				sub_products = sub_cat.product_set.all()
				for product in sub_products:
					products.add(product)

		# selected_values = []
		# active_filters = []
		# for key, value in request.session.items():
		# 	# بررسی آیا کلید با الگوی مورد نظر شروع می‌شود
		# 	if key.startswith('filter-'):
				
		# 		filter_name = key.replace('filter-', '')
		# 		selected_filter = Filter.objects.get( name = filter_name)
		# 		for posi_value in selected_filter.value.all():
		# 			if posi_value.value in value:
		# 				new_active_filter = {'filter':selected_filter,'value':posi_value}
		# 				active_filters.append(new_active_filter)
		# 				selected_values.append(posi_value.id)
		# products = Product.get_filtered_products(Product ,selected_values)
		products = list(products)
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		paginator = Paginator(products, 12)
		page = request.GET.get('page', 1)
		brands = category.get_category_brands()
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)

		colors = ProductColor.objects.all()
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				{'products': products, 
	 			'colors': colors,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges,
				'category':category,
				'filters':filters,
				'brands': brands,
				'my_forms':my_forms,
				# 'active_filters':active_filters,
				'main_selected_category': category
				})
		
class ProductDetailView(View):

	def get(self, request, product_slug ):
		store = Store.objects.get(name=store_name)
		product = Product.objects.filter(slug = product_slug).first()
		if product.views:
			product.views = product.views + 1
		else:
			product.views = 1
		product.save()
		varieties = Variety.objects.filter(product=product)
		message = ''
		form = PurchaseForm()
		comments = Comment.objects.filter(product=product)
		services = Services.objects.all()
		if isinstance(request.user, AnonymousUser):
			for key, value in request.session.items():
					if str(product.id)==key:
						message = f'شما در حال حاضر {value} عدد از این کالا را در سبد خرید خود دارید.'
		else:
			customer = Customer.objects.get(phone_number = request.user.phone_number)
			cart , create= Cart.objects.get_or_create(customer = customer)
			cart_item = cart.items.filter(variety__in = varieties).first()
			if cart_item != None:
				message = f'شما در حال حاضر {cart_item.quantity} عدد از این کالا را در سبد خرید خود دارید.'
		
		add_to_cart_url = f'{current_app_name}:add-to-cart'
		products = product.get_related_products()
		brand = Brand.objects.get(name = product.brand)
		return render(request, f'{current_app_name}/product_detail_{store.template_index}.html', 
				{'brand':brand,'services':services,'products':products,'product': product,'comments':comments ,'varieties':varieties,'form':form, 'message':message, 'add_to_cart':add_to_cart_url, 'store_name':store_name})

class CommentCreateView(IsCustomerUserMixin, View):

	def post(self, request, product_id):
		customer = Customer.objects.get(phone_number=request.user.phone_number)
		product = get_object_or_404(Product, id=product_id)
		form = CommentForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			body = form.cleaned_data['body']
			comment = Comment.objects.create(
				product=product,
				sender=customer,
				email=email,
				body=body,
			)
			comment.save()
			return redirect('shop:product_detail', product.slug)  # Redirect to the product detail page
		return redirect('shop:product_detail', product.slug)
	

	def get(self, request, comment_id, status_id, *args, **kwargs):
		store = Store.objects.get(name=store_name)
		comment = Comment.objects.get(id=comment_id)
		product = comment.product
		
		if status_id == 1:
			comment.approved = True
			comment.save()
		else:
			comment.approved = False
			comment.save()
		
		return redirect(f'{current_app_name}:owner_dashboard_comments')

class CartView(IsCustomerUserMixin, View):

	def get(self, request, cart_id):
		store = Store.objects.get(name=store_name)
		customer = Customer.objects.filter(phone_number=request.user.phone_number).first()
		cart = Cart.objects.filter(id=cart_id).first()
		form = PurchaseForm
		edit_cart_url = f"{current_app_name}:cart_item_update' cart_id=cart.pk item_id=item.pk "
		return render(request, f'{current_app_name}/cart_{store.template_index}.html',
				 {'form': form, 'cart': cart, 'edit_cart':edit_cart_url, 'store_name':store_name})

	def post(self, request, cart_id, *args, **kwargs):
		item_id = kwargs['item_id']
		store = Store.objects.get(name=store_name)
		form = CartEditForm(request.POST)
		cart = Cart.objects.filter(id=cart_id).first()
		cart_item = cart.items.filter(id=item_id).first()
		if form.is_valid():
			cart_item.quantity = form.cleaned_data['count']
			cart_item.save()
			cart.save
			return redirect(f'{current_app_name}:cart_view', cart_id)
		edit_cart_url = f"{current_app_name}:cart_item_update' cart_id=cart.pk item_id=item.pk "
		return render(request, f'{current_app_name}/cart_{store.template_index}.html',
				 {'cart': cart, 'message': 'Something is going wrong', 'edit_cart':edit_cart_url, 'store_name':store_name})

class AddToCartView(View):
	
	message =''

	def post(self, request, pk, *args, **kwargs):
		form = PurchaseForm(request.POST)
		store = Store.objects.get(name = store_name)
		if form.is_valid():
			replicate = False
			product = Product.objects.get(pk = pk)
			quantity = form.cleaned_data['count']
			size = form.cleaned_data['size']
			
			if size == '':
				default_variety = Variety.objects.filter(product=product, name = 'default variety').first()
				variety_id = default_variety.id
				variety = default_variety
			else:
				variety_id = int(form.cleaned_data['size'])
				variety = Variety.objects.get(id = variety_id)

			if size=='0':
				varieties = Variety.objects.filter(product=product)
				add_to_cart_url = f'{current_app_name}:add-to-cart'
				return render(request, f'{current_app_name}/product_detail_{store.template_index}.html', {'message':'لطفا تنوع مورد نظر خود را انتخاب نمایید.','product': product, 'varieties':varieties,'form':form, 'add_to_cart':add_to_cart_url, 'store_name':store_name})
			
			
			if quantity>variety.stock:
				varieties = Variety.objects.filter(product=product)
				add_to_cart_url = f'{current_app_name}:add-to-cart'
				return render(request,  f'{current_app_name}/product_detail_{store.template_index}.html', {'message':f'از این تنوع تنها {variety.stock} عدد در انبار موجود است.','product': product, 'varieties':varieties,'form':form, 'add_to_cart':add_to_cart_url, 'store_name':store_name})
			
			new_item = {'product': product, 'quantity': quantity}
			if isinstance(request.user, AnonymousUser):
		
				for key, value in request.session.items():
					if str(variety.id)==key:
						request.session[str(variety.id)] += quantity
						replicate = True
						break
					
				if replicate == False:
					request.session.update({variety.id: quantity})
			else:
				customer = Customer.objects.filter(phone_number = request.user.phone_number).first()
				cart, create = Cart.objects.get_or_create(customer = customer)
				if cart.items.filter(variety=variety).exists():
					cart_item = cart.items.get(variety=variety)
					cart_item.quantity = quantity
					cart_item.save()
				else:
					cart_item = CartItem.objects.create(variety=variety, quantity=quantity)
				
				cart.items.add(cart_item)

			return redirect(f'{current_app_name}:product_detail' ,product.slug)

class CustomerRegisterLoginView(View):
	
	template_name = f'{current_app_name}/register-customer.html'
	message = 'Please Insert Your Phone Number'

	def get(self, request):
		form = RequestNumberForm()
		return render(request, self.template_name, {'form': form, 'message':self.message})

	def post(self, request):
		form = RequestNumberForm(request.POST)
		store = Store.objects.get(name = store_name)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			customer = Customer.objects.filter(phone_number=phone_number).first()
			authen_form = AuthenticationCodeForm()
			if customer != None:
				previous_codes = OtpCode.objects.filter(phone_number = phone_number)
				previous_codes.delete()
				random_code = random.randint(100000,999999)
				send_otp_code(phone_number,random_code)
				new_otp = OtpCode.objects.create(phone_number = phone_number, code = random_code) 
				return redirect(f'login/{phone_number}')
			customer = Customer.objects.create(phone_number = phone_number)
			user = User.objects.get_or_create(phone_number = phone_number)
			previous_codes = OtpCode.objects.filter(phone_number = phone_number)
			previous_codes.delete()
			random_code = random.randint(100000,999999)
			send_otp_code(phone_number,random_code)
			new_otp = OtpCode.objects.create(phone_number = phone_number, code = random_code) 
			return redirect(f'login/{phone_number}')
		message = 'Invalid Input'
		return render(request, self.template_name, {'message':message, 'form':form})

class CustomerloginView(View):
	template_name = f'{current_app_name}/login.html'

	def get(self, request, phone_number):
		form = AuthenticationCodeForm()
		return render(request, self.template_name, {'form':form})
	
	def post(self, request, phone_number, *args, **kwargs):
		form = AuthenticationCodeForm(request.POST)
		if form.is_valid():
			customer_phone = phone_number
			store = Store.objects.get(name=store_name)
			customer = Customer.objects.filter(phone_number = customer_phone).first()
			user = User.objects.filter(phone_number = customer_phone).first()
			request.user = user
			last_sent_otp = OtpCode.objects.filter(phone_number = customer_phone).first()
			recieved_code = form.cleaned_data['code']
			if last_sent_otp.code == recieved_code:
				customer.otp_token = form.cleaned_data['code']
				customer.save()
				login(request, user)
				cart, created = Cart.objects.get_or_create(customer = customer)
				varieties = Variety.objects.all()
				varieties_id_list = []
				for variety in varieties:
					varieties_id_list.append(str(variety.id))
				for key, value in request.session.items():
					if key in varieties_id_list:
						variety = Variety.objects.filter(id = int(key)).first()
						if cart.items.filter(variety=variety).exists():
							cart_item = cart.items.get(variety=variety)
							cart_item.quantity = value
							cart_item.save()
						else:
							cart_item = CartItem.objects.create(variety=variety, quantity=value)
							cart.items.add(cart_item)
				for key in list(request.session.keys()):
					if key in varieties_id_list:
						del request.session[key]
				
				return redirect(f'{current_app_name}:index')
			return render(request, self.template_name, {'form':form, 'message':'wrong code'})
		return render(request, self.template_name, {'form':form, 'message':'Invalid Input'})

class CustomerOrdersView(IsCustomerUserMixin, View):

	def get(self, request):
		store = Store.objects.get(name = store_name)
		customer = Customer.objects.filter(phone_number=request.user.phone_number).first()
		orders = Order.objects.filter(customer=customer)
		return render(request, f'{current_app_name}/customer-dashboard-orders_{store.template_index}.html', {'orders':orders})
	
class CustomerFavoritesView(IsCustomerUserMixin, View):

	def get(self, request):
		fav_products = None
		store = Store.objects.get(name = store_name)
		customer = Customer.objects.filter(phone_number=request.user.phone_number).first()
		if customer != None:
			fav_products = customer.favorites.all()
			return render(request, f'{current_app_name}/customer_favorites_{store.template_index}.html', {'fav_products':fav_products, 'message':'Favorite Products'})
		return render(request, f'{current_app_name}/customer_favorites_{store.template_index}.html', {'fav_products':fav_products, 'message':'You should sign in first'})

class DeleteCartItemView(View):

	def  get(self, request, cart_id, item_id, *args, **kwargs):
		cart_item = CartItem.objects.get(id=item_id)
		cart_item.delete()
		return redirect(f'{current_app_name}:cart_view', cart_id)

class OrderWrongCouponView(IsCustomerUserMixin, View):

	form_class = CouponApplyForm

	def get(self, request, order_id,wrong_code):
		order = get_object_or_404(Order, id=order_id)
		store = Store.objects.get(name = store_name)
		order_detail_url = f"{current_app_name}:apply_coupon"
		delivery_methods = Delivery.objects.all()
		form2 = DeliveryApplyForm
		message = 'کد وارد شده اشتباه و یا منقضی است.'
		return render(request, f'{current_app_name}/order_detail_{store.template_index}.html', {'form2':form2,'delivery_methods':delivery_methods ,'order':order, 'form':self.form_class, 'order_detail':order_detail_url, 'store_name':store_name,'message':message})

class CouponApplyView(IsCustomerUserMixin, View):

	form_class = CouponApplyForm
	current_datetime = datetime.now()
	def post(self, request, order_id, *args, **kwargs):

		order = Order.objects.get(id=order_id)
		form = self.form_class(request.POST)
		if form.is_valid():
			code = form.cleaned_data['code']
			store = Store.objects.get(name = store_name)
			coupon = Coupon.objects.filter(code__exact=code).first()
			if order.used_coupon == True:
				order.delivery_description = order.delivery_description + f'<p class="text-danger">برای این سفارش قبلا کد تخفیف وارد شده است</p><br>' 
				order.save()
				return redirect(f'{current_app_name}:order_final_check', order_id)
			if coupon == None:
				order.delivery_description = order.delivery_description + f'<p class="text-danger">کد تخفیف نامعتبر</p><br>' 
				order.save()
				return redirect(f'{current_app_name}:order_final_check', order_id)
			if coupon.is_valid():
				order.total_price -= coupon.discount
				order.used_coupon = True
				order.delivery_description = order.delivery_description + f'<p class="text-success">مبلغ نهایی پس از اعمال کد تخفیف: {order.total_price+order.delivery_cost:,} تومان</p>' 
				order.save()
				return redirect(f'{current_app_name}:order_final_check', order_id)
		order.delivery_description = order.delivery_description + f'<p class="text-danger">کد وارد شده نامعتبر بوده و یا قبلا وارد شده است</p><br>' 
		order.save()
		return redirect(f'{current_app_name}:order_final_check', order_id)
	
	template_name = f'{current_app_name}/owner-dashboard-coupons.html'

class AboutUsPageView(View):

	def get(self, request):
		store = Store.objects.get(name = store_name)
		logo = StoreLogoImage.objects.all().first()
		return render(request, f'{current_app_name}/about_{store.template_index}.html', {'logo':logo,'description':store.about_description})

class ContactUsPageView(View):

	def get(self, request):
		store = Store.objects.get(name = store_name)
		return render(request, f'{current_app_name}/contact_{store.template_index}.html', {'store':store})

	def post(self, request, *args, **kwargs):
		form = ContactUsForm(request.POST)
		store = Store.objects.get(name = store_name)
		if form.is_valid():
			
			name = form.cleaned_data['name']
			familly_name = form.cleaned_data['familly_name']
			email = form.cleaned_data['email']
			phone = form.cleaned_data['phone']
			subject = form.cleaned_data['subject']
			message_text = form.cleaned_data['message_text']

			new_message = ContactMessage.objects.create(
				name = name,
				
				familly_name=familly_name,
				email=email,
				phone=phone,
				subject=subject,
				message=message_text
			)
			return render(request, f'{current_app_name}/contact_{store.template_index}.html', {'message':'پیام شما با موفقیت ارسال گردید.'})
		return render(request, f'{current_app_name}/contact_{store.template_index}.html', {'message':'مقادیر به درستی وارد نشده‌اند.'})

class ProductSearchView(View):

	def get(self, request, *args, **kwargs):
		store = Store.objects.get(name=store_name)
		query = request.GET.get('q')
		if query:
			
			products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).distinct()
		else:
			products = Product.objects.all()

		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		categories = Category.objects.all()
		# paginator = Paginator(products, 12)
		# page = request.GET.get('page', 1)
		# try:
		# 	products = paginator.page(page)
		# except PageNotAnInteger:
		# 	products = paginator.page(1)
		# except EmptyPage:
		# 	products = paginator.page(paginator.num_pages)
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', {'products': products, 
													'query': query, 
													'to_products':products_urls, 
													'store_name':store_name, 
													'categories':categories,
													'sizes':sizes,
													'price_ranges':price_ranges})

class FaqView(View):

	def get(self, request, *args, **kwargs):
		store = Store.objects.get(name=store_name)
		faqs = Faq.objects.all()
		return render(request, f'{current_app_name}/faq_{store.template_index}.html', {'store_name':store_name, 'faqs':faqs})
	
class BlogView(View):

	def get(self, request, *args, **kwargs):
		store = Store.objects.get(name=store_name)
		posts = BlogPost.objects.all()
		products = Product.objects.all()
		blog_categories = BlogCategory.objects.all()
		return render(request, f'{current_app_name}/blog_{store.template_index}.html', {'store_name':store_name,
											  'store':store,
											  'posts':posts,
											  'products':products,
											  'blog_categories':blog_categories})
	
class BlogPostDetailView(View):

	def get(self, request, post_slug, *args, **kwargs):
		store = Store.objects.get(name = store_name)
		post = BlogPost.objects.get(slug = post_slug)
		posts = BlogPost.objects.all()
		blog_categories = BlogCategory.objects.all()
		return render(request, f'{current_app_name}/blog-detail_{store.template_index}.html', {'store':store,
											  'post':post,
											  'posts':posts,
											  'blog_categories':blog_categories})

class SubscribeView(IsCustomerUserMixin, View):

	def post(self, request, *args, **kwargs):
		form = SubscriptionForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			store = Store.objects.get(name = store_name)
			new_subscriber, create = Subscription.objects.get_or_create( email=email)
			return redirect(f'{current_app_name}:index')

class PoliciesView(View):

	def get(self, request):
		store = Store.objects.get(name = store_name)
		return render(request, f'{current_app_name}/policies_{store.template_index}.html', {'store':store})
	
class FilterView(View):

	template_name = f'{current_app_name}/owner-dashboard-filters.html'

	def get(self, request):
		form = AddFilterForm
		store = Store.objects.get(name = store_name)
		categories = Category.objects.all()
		filters = Filter.objects.all()
		return render(request, self.template_name, {'store':store, 'store_name':store_name, 'filters':filters, 'form':form, 'categories':categories})

	def post(self, request, *args, **kwargs):
		form = AddFilterForm(request.POST)
		if form.is_valid():
			store = Store.objects.get(name = store_name)
			category = Category.objects.get( name=form.cleaned_data['category'])
			new_filter, create = Filter.objects.get_or_create(
				category = category,
				name = form.cleaned_data['name'],
				store = store
			)
			return redirect(f'{current_app_name}:owner_dashboard_filters')
		
class AsignFilterToProductView(View):

	def post(self, request, product_id, *args, **kwargs):
		form = AsignFilterToProductForm(request.POST)
		if form.is_valid():
			store = Store.objects.get(name = store_name)
			product = Product.objects.get(id = product_id)
			filter = Filter.objects.get(store = store , name = form.cleaned_data['filter'])
			new_filter_asign , create= FilterValue.objects.get_or_create(
				 
				value = form.cleaned_data['value'] 
			)
			new_filter_asign.product.add(product)
			filter.value.add(new_filter_asign)
			filter.save()
			return redirect(f'{current_app_name}:product_update', product.id)

form_classes = [type(f'FeatureFilterForm{i}', (FeatureFilterForm,), {}) for i in range(1, 4)]

class FeatureFilterView(View):
	def post( self , request, category_slug, form_name):
		store = Store.objects.get(name = store_name)
		category = Category.objects.get( slug = category_slug)
		filter = Filter.objects.filter( name = form_name).first()
		values = filter.value.all()
		class FeatureFilterForm(forms.Form):
			name = filter.name
			choices = tuple([(value.value, value.value) for value in values])
			فیلترها = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
		form = FeatureFilterForm(request.POST)
		if form.is_valid():
			products = Product.objects.filter(category=category)
			categories = Category.objects.all()
			sizes = Size.objects.all()
			price_ranges  = PriceRange.objects.all()
			filters = Filter.objects.all()
			request.session.modified = True
			request.session[f'filter-{filter.name}'] = form.cleaned_data['فیلترها']
			request.session['temp_cat'] = category.name
			request.session.modified = True
			my_forms = []
			for filter in filters:
				values = filter.value.all()
				class FeatureFilterForm(forms.Form):
					name = filter.name
					choices = tuple([(value.value, value.value) for value in values])
					فیلترها = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
				new_form = FeatureFilterForm
				my_forms.append(new_form)
			
			selected_values = []
			active_filters = []
			for key, value in request.session.items():
				# بررسی آیا کلید با الگوی مورد نظر شروع می‌شود
				if key.startswith('filter-'):
					
					filter_name = key.replace('filter-', '')
					selected_filter = Filter.objects.get( name = filter_name)
					for posi_value in selected_filter.value.all():
						if posi_value.value in value:
							new_active_filter = {'filter':selected_filter,'value':posi_value}
							active_filters.append(new_active_filter)
							selected_values.append(posi_value.id)
			products = Product.get_filtered_products(Product ,selected_values)

			return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				{'products': products, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges,
				'category':category,
				'filters':filters,
				'my_forms':my_forms,
				'active_filters':active_filters,
				})

class ClearActiveFilterValueView(View):

	def get(self, request, filter_id, value_id):
		active_filter = Filter.objects.get(id = filter_id)
		category = active_filter.category
		active_value = FilterValue.objects.get(id = value_id)
		for key, value in request.session.items():
			if active_filter.name in key and active_value.value in value:
				if len(value) == 1:
					del request.session[key]
				else:
					value.remove(active_value.value)
				request.session.modified = True

				return redirect(f'{current_app_name}:category_products', category.slug )

def format_features(features_list):
	output = ""
	for feature in features_list:
		title = feature['title']
		values = feature['values']
		values_str = ', '.join(values)  
		output += f"{title}: {values_str}<br>"
	return output

def download_and_save_images(image_urls, product_id):
	product = Product.objects.get(id=product_id)
	store = product.store
	for url in image_urls:
		response = requests.get(url)
		if response.status_code == 200:
			image_name = product.name
			image_filename = image_name
			image = ProductImage(
				product=product,
			)
			image.image.save(image_filename, ContentFile(response.content))
			image.save()

def download_and_save_main_image(image_url, product_id):
	product = Product.objects.get(id=product_id)
	store = product.store
	url = image_url
	response = requests.get(url)
	if response.status_code == 200:
		image_name = product.name
		image_filename = image_name
		image = ProductImage(
			product=product,
		)
		image.image.save(image_filename, ContentFile(response.content))
		image.save()

class AddProductFromDigikalaView(View):

	def post(self, request):

		form = AddingProductFromDigiForm(request.POST)
		if form.is_valid():
			category_list = request.POST.getlist('category')
			dkp_code = form.cleaned_data['dkp_code']
			numbers = dkp_code.split("-")
			numbers = [int(num) for num in numbers]
			for dkp_code in numbers:
				url = f'https://api.digikala.com/v2/product/{dkp_code}/'
				shop_name = f'{Store.objects.all().first().name}'
				try:
					response = requests.get(url)
					response.raise_for_status()
					item = response.json()['data']['product']
					brand = ''
					title = ''
					features= []
					description = ''
					price = 0
					tags = []
					images = []
					main_image = ''

					if item['specifications'][0] == [] or item['specifications'][0] == None:
						features = []
					else:
						features= item['specifications'][0]['attributes']
					brand = item['data_layer']['brand']
					title = item['title_fa']
					title = title.replace("/", "")
					words = title.split()
					if len(words) > 15:
						words = words[:15]
					title = " ".join(words)
					price = item['default_variant']['price']['selling_price']
					tags = [tag['name'] for tag in item['tags']]
					images = [image['url'][0].replace('?x-oss-process=image/resize,m_lfit,h_800,w_800/quality,q_90','').replace(' ','') for image in item['images']['list']]
					main_image = item['images']['main']['url'][0].replace('?x-oss-process=image/resize,m_lfit,h_800,w_800/quality,q_90',''),
					main_image = main_image[0]
					description = item['review']['description']
				except requests.exceptions.HTTPError as err:
					print(f'HTTP error occurred: {err}')
				except Exception as err:
					print(f'Other error occurred: {err}')

				store = Store.objects.all().first()
				if not description:
					description = '-'
				slug = title.replace(' ','-')
				description = description
				features = features
				brand = brand
				product_brand, create = Brand.objects.get_or_create(
					name = brand,
					store = store
				)
				price = price/10
				tags = tags
				new_product = Product.objects.create(
					name = title,
					
					slug = slug,
					description = description,
					features = format_features(features),
					brand = product_brand.name,
					price = price,
				)
				for category_id in category_list:
					if category_id == '0':
						category, create = Category.objects.get_or_create(
																			name = 'دسته‌بندی نشده',
																			slug = 'ungategorized')
					else:
						category = Category.objects.get(id = category_id)
					new_product.category.add(category)
					new_product.save()
				images = images
				download_and_save_main_image(main_image, new_product.id)
				download_and_save_images(images, new_product.id)
				default_variety = Variety.objects.create(
					name = 'default variety',
					product = new_product, 
					stock = 2,
				)
		return redirect('shop:product_list')				
					
class SpecialProductListView(View):

	def get(self, request, tag_name):
		tag = Tag.objects.filter(name=tag_name).first()
		products = tag.get_products()
		items_per_page = 12
		store = Store.objects.get(name=store_name)
		categories = Category.objects.all()
		paginator = Paginator(products, items_per_page)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		brands = Brand.objects.all()
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				{'products': products, 
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'brands':brands,
				'sizes':sizes,
				'price_ranges':price_ranges})
	
	def post(self, request, tag_name, *args, **kwargs):
		main_filters = {}
		filters = []
		product_cat = None
		price_range = None
		selected_brand = None
		tag = Tag.objects.filter(name=tag_name).first()
		products = tag.get_products()
		form = FilterProductsForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			store = Store.objects.get(name=store_name)
			category = form.cleaned_data['category']
			if category != '':
				product_cat = Category.objects.filter(id = int(category)).first()
				if category != '0':
					products = products.filter(category = product_cat)
				else:
					products = products.all()
				
			brand = form.cleaned_data['brand']
			if brand != '':
				selected_brand = Brand.objects.filter(id = brand).first()
				if brand != '0':
					products = products.filter(brand = selected_brand.name)
				else:
					products = products.all()
							
			filtered_products = []
			price_ranges = form.cleaned_data['price_range']
			if price_ranges != '0':
				for price in price_ranges:
					selected_price_range = PriceRange.objects.filter(id = int(form.cleaned_data['price_range'])).first()
			else:
				selected_price_range = None

			if selected_price_range != None:
				for product in products:
								if product.price<selected_price_range.max_value and product.price>=selected_price_range.min_value:
									filtered_products.append(product.id)
			
			if filtered_products != []:
				products = products.filter(id__in=filtered_products)

			if selected_price_range != None and filtered_products == []:
				products = []
			categories = Category.objects.all()
			store = Store.objects.get(name=store_name)
			products_urls = f'{current_app_name}:product_detail'
			sizes = Size.objects.all()
			price_ranges = PriceRange.objects.all()
			brands = Brand.objects.all()
			if brand != '0':
				selected_brand = Brand.objects.get(id=brand)
			else:
				selected_brand = None

			my_forms = []
			if category != '0':
				selected_category = Category.objects.filter(id = int(category)).first()
				filters = Filter.objects.all()
				for filter in filters:
					values = filter.value.all()
					class FeatureFilterForm(forms.Form):
						name = filter.name
						choices = tuple([(value.value, value.value) for value in values])
						فیلترها = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
					new_form = FeatureFilterForm
					my_forms.append(new_form)
				category = Category.objects.get(slug = selected_category.slug)
				filters = Filter.objects.filter(category=category)
			else:
				selected_category = None

			selected_values = []
			active_filters = []
			for key, value in request.session.items():
				if key.startswith('filter-'):
					
					filter_name = key.replace('filter-', '')
					selected_filter = Filter.objects.get( name = filter_name)
					for posi_value in selected_filter.value.all():
						if posi_value.value in value:
							new_active_filter = {'filter':selected_filter,'value':posi_value}
							active_filters.append(new_active_filter)
							selected_values.append(posi_value.id)

			paginator = Paginator(products, 12)
			page = request.GET.get('page', 1)
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				# اگر شماره صفحه یک عدد نیست
				products = paginator.page(1)
			except EmptyPage:
				# اگر شماره صفحه بیشتر از تعداد کل صفحات است
				products = paginator.page(paginator.num_pages)

			return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				 {'products': products, 
				'brands':brands,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges,
				'selected_brand':selected_brand,
				'selected_price_range':selected_price_range,
				'selected_category':selected_category,
				'filters':filters,
				'category':selected_category,
				'my_forms':my_forms,
				'active_filters':active_filters,
				'main_filters': main_filters,
				'main_selected_category' : product_cat,
				'main_selected_brand' : selected_brand,
				'main_selected_price_range' : selected_price_range})
					
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', {'store_name':store_name})

class BrandProductListView(View):

	def get(self, request, brand_name):
		brand = Brand.objects.filter(name=brand_name).first()
		products = Product.objects.filter(brand=brand.name, verified = True)
		items_per_page = 12
		store = Store.objects.get(name=store_name)
		categories = Category.objects.all()
		paginator = Paginator(products, items_per_page)
		page = request.GET.get('page', 1)
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			products = paginator.page(1)
		except EmptyPage:
			products = paginator.page(paginator.num_pages)
		brands = Brand.objects.all()
		products_urls = f'{current_app_name}:product_detail'
		sizes = Size.objects.all()
		price_ranges = PriceRange.objects.all()
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				{'products': products, 
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'brands':brands,
				'sizes':sizes,
				'price_ranges':price_ranges})
	
	def post(self, request, brand_name, *args, **kwargs):
		main_filters = {}
		filters = []
		product_cat = None
		price_range = None
		
		brand = Brand.objects.filter(name=brand).first()
		products = Product.objects.filter(brand=brand.name)
		selected_brand = brand
		form = FilterProductsForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			store = Store.objects.get(name=store_name)
			category = form.cleaned_data['category']
			if category != '':
				product_cat = Category.objects.filter(id = int(category)).first()
				if category != '0':
					products = products.filter(category = product_cat)
				else:
					products = products.all()
				
			brand = form.cleaned_data['brand']
			if brand != '':
				selected_brand = Brand.objects.filter(id = brand).first()
				if brand != '0':
					products = products.filter(brand = selected_brand.name)
				else:
					products = products.all()
							
			filtered_products = []
			price_ranges = form.cleaned_data['price_range']
			if price_ranges != '0':
				for price in price_ranges:
					selected_price_range = PriceRange.objects.filter(id = int(form.cleaned_data['price_range'])).first()
			else:
				selected_price_range = None

			if selected_price_range != None:
				for product in products:
								if product.price<selected_price_range.max_value and product.price>=selected_price_range.min_value:
									filtered_products.append(product.id)
			
			if filtered_products != []:
				products = products.filter(id__in=filtered_products)

			if selected_price_range != None and filtered_products == []:
				products = []
			categories = Category.objects.all()
			store = Store.objects.get(name=store_name)
			products_urls = f'{current_app_name}:product_detail'
			sizes = Size.objects.all()
			price_ranges = PriceRange.objects.all()
			brands = Brand.objects.all()
			if brand != '0':
				selected_brand = Brand.objects.get(id=brand)
			else:
				selected_brand = None

			my_forms = []
			if category != '0':
				selected_category = Category.objects.filter(id = int(category)).first()
				filters = Filter.objects.all()
				for filter in filters:
					values = filter.value.all()
					class FeatureFilterForm(forms.Form):
						name = filter.name
						choices = tuple([(value.value, value.value) for value in values])
						فیلترها = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
					new_form = FeatureFilterForm
					my_forms.append(new_form)
				category = Category.objects.get(slug = selected_category.slug)
				filters = Filter.objects.filter(category=category)
			else:
				selected_category = None

			selected_values = []
			active_filters = []
			for key, value in request.session.items():
				if key.startswith('filter-'):
					
					filter_name = key.replace('filter-', '')
					selected_filter = Filter.objects.get( name = filter_name)
					for posi_value in selected_filter.value.all():
						if posi_value.value in value:
							new_active_filter = {'filter':selected_filter,'value':posi_value}
							active_filters.append(new_active_filter)
							selected_values.append(posi_value.id)

			paginator = Paginator(products, 12)
			page = request.GET.get('page', 1)
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				# اگر شماره صفحه یک عدد نیست
				products = paginator.page(1)
			except EmptyPage:
				# اگر شماره صفحه بیشتر از تعداد کل صفحات است
				products = paginator.page(paginator.num_pages)

			return render(request, f'{current_app_name}/product_list_{store.template_index}.html', 
				 {'products': products, 
				'brands':brands,
				'to_products':products_urls, 
				'store_name':store_name, 
				'categories':categories,
				'sizes':sizes,
				'price_ranges':price_ranges,
				'selected_brand':selected_brand,
				'selected_price_range':selected_price_range,
				'selected_category':selected_category,
				'filters':filters,
				'category':selected_category,
				'my_forms':my_forms,
				'active_filters':active_filters,
				'main_filters': main_filters,
				'main_selected_category' : product_cat,
				'main_selected_brand' : selected_brand,
				'main_selected_price_range' : selected_price_range})
					
		return render(request, f'{current_app_name}/product_list_{store.template_index}.html', {'store_name':store_name})

class CreateOrderView(IsCustomerUserMixin, View):

	def get(self, request):
		message = ''
		store = Store.objects.get(name = store_name)
		customer = Customer.objects.filter(phone_number=request.user.phone_number).first()
		cart = Cart.objects.filter(customer=customer).first()
		if cart.items.all().first() != None:
			items = cart.items.all()
			total_price = 0
			order_status = OrderStatus.objects.get(pk=2)
			for item in items:
				price = item.variety.product.get_active_price()*item.quantity
				total_price += price
			order = Order.objects.create(customer=customer, total_price=total_price, status = order_status)
			order.items.set(items)
			for item in order.items.all():
				if item.variety.product.express == True:
					order.has_express_items = True
					order.save()
					break
			for item in order.items.all():
				if item.variety.product.express == False:
					order.has_normal_items = True
					order.save()
					break
			cart.items.clear()
			return redirect(f'{current_app_name}:order_detail' , order.id)
		return render(request, f'{current_app_name}/empty-cart_{store.template_index}.html', {'store_name':store_name})

class OrderDetailView(IsCustomerUserMixin ,View):

	def get(self, request, order_id):
		form = OrderDeliveryOptionsForm
		order = Order.objects.get(id=order_id)
		order_detail_url = f"{current_app_name}:apply_coupon"
		delivery_mthods = []
		for delivery in Delivery.objects.all():
			if order.total_price <= delivery.min_cart_free:
				price = f'{delivery.price:,} تومان'
			else:
				price = 'رایگان'
			new_del = {
				'id': delivery.id,
				'name': delivery.name,
				'price': price,
			}
			delivery_mthods.append(new_del)
		
		return render(request, f'{current_app_name}/order_detail_{store.template_index}.html', {'form':form,
																								'order':order, 
																								'order_detail':order_detail_url, 
																								'store_name':store_name,
																								'delivery_mthods':delivery_mthods})
	def post(self, request, order_id):
		store = Store.objects.all().first()
		form = OrderDeliveryOptionsForm(request.POST)
		order = Order.objects.get(id = order_id)
		if form.is_valid():
			print('KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK')
			print(form.cleaned_data)
			delivery_method = Delivery.objects.get(id = int(form.cleaned_data['delivery_method']))
			order.delivery_method = delivery_method
			delivery_description = ''
			delivery_description = delivery_description+'اقلام سفارش: <br>'
			for item in order.items.all():
				delivery_description = delivery_description+f'{item.variety.product.name} - تنوع: {item.variety.name.replace('default variety','ندارد')} - قیمت: {item.get_item_price():,} تومان - تعداد: {item.quantity} عدد - مجموع هزینه: {item.get_item_price()*item.quantity:,} تومان<br>'
			delivery_description = delivery_description+'شیوه ارسال: <br>'
			if order.total_price <= delivery_method.min_cart_free:
				delivery_description = delivery_description+f'{delivery_method.name} + {delivery_method.price:,} تومان  <br>'
				order.delivery_cost = delivery_method.price
				delivery_cost = delivery_method.price
			else:
				delivery_description = delivery_description+f'{delivery_method.name}، هزینه رایگان <br>'
				order.delivery_cost = 0
				delivery_cost = 0
			delivery_description = delivery_description + '---------------------------------------------<br>'
			delivery_description = delivery_description + f'هزینه کالاهای سفارش: {order.total_price:,} تومان<br>'
			delivery_description = delivery_description + '---------------------------------------------<br>'
			if order.total_price <= delivery_method.min_cart_free:
				delivery_description = delivery_description+f'هزینه ارسال: {delivery_method.price:,} تومان  <br>'
			else:
				delivery_description = delivery_description+f'هزینه ارسال: رایگان <br>'
			delivery_description = delivery_description + '---------------------------------------------<br>'
			delivery_description = delivery_description + f'مجموع هزینه: {order.total_price+delivery_cost:,} تومان<br>'
			order.delivery_description = delivery_description
			order.save()
			return redirect('shop:order_reciever_detail', order.id)

class RecieverDetailsView(View):

	template_name = f'{current_app_name}/reciever_details.html'

	def get(self, request, order_id):
		form = RecieverDetailsForm
		store = Store.objects.get(name = store_name)
		order = Order.objects.get(id = order_id)
		return render(request, self.template_name, {'order':order, 'store':store, 'form':form})

	def post(self, request, order_id):

		form = RecieverDetailsForm(request.POST)
		store = Store.objects.get(name = store_name)
		order = Order.objects.get(id = order_id)
		if form.is_valid():
			order.reciever_name = form.cleaned_data['name']
			order.reciever_familly_name =form.cleaned_data['familly_name']
			order.reciever_phone_number = form.cleaned_data['phone_number']
			order.reciever_email = form.cleaned_data['email']
			order.reciever_state = form.cleaned_data['state']
			order.reciever_city = form.cleaned_data['city']
			order.reciever_zip_code = form.cleaned_data['zip_code']
			order.reciever_address = form.cleaned_data['address']
			order.save()
			return redirect('shop:order_final_check', order.id)

class OrderFinalCheckView(View):

	def get(self, request, order_id):
		result = ''
		store = Store.objects.all().first()
		order = Order.objects.get(id = order_id)
		delivery_des = order.delivery_description
		if 'text-success' in delivery_des:
			lines = delivery_des.split('<br>')
			for line in lines:
				print(line)
				if 'text-danger' not in line or 'مبلغ نهایی' in line:
					result = result + f'{line}<br> '
			order.delivery_description = result
			order.save()
		return render(request, f'{current_app_name}/order_final_check_{store.template_index}.html', {'store':store, 'order':order})
	

class OrderPayView(IsCustomerUserMixin, View):
	
	def get(self, request, order_id, *args, **kwargs):

		store = Store.objects.get(name = store_name)
		order = Order.objects.get(id=order_id)
		request.session['order_pay'] = {
			'order_id': order.id,
		}

		if order.get_final_payment() == 0:
			order.status = OrderStatus.objects.get(id=1)
			customer = order.customer
			customer.wallet_balance -= order.get_without_cashback_cost()
			customer.save()
			order.paid_by_wallet = order.get_without_cashback_cost()
			order.save()
			return redirect(f'{current_app_name}:customer_dashboard_order_detail', order.id)
		MERCHANT = store.merchant
		req_data = {
			"merchant_id": MERCHANT,
			"amount": order.get_final_payment()*10,
			"callback_url": f'https://picosite.ir/shop/{store_name}/orders/verify/',
			"description": description,
			"metadata": {"mobile": request.user.phone_number, "email": request.user.email}
		}
		req_header = {"accept": "application/json",
					"content-type": "application/json'"}
		req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
			req_data), headers=req_header)
		authority = req.json()['data']['authority']
		if len(req.json()['errors']) == 0:
			return redirect(ZP_API_STARTPAY.format(authority=authority))
		else:
			e_code = req.json()['errors']['code']
			e_message = req.json()['errors']['message']
			return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

class OrderVerifyView(LoginRequiredMixin, View):

	template_name = f'{current_app_name}/customer-payment-result.html'

	def get(self, request):
		paid_status = OrderStatus.objects.get(id=1)
		order_id = request.session['order_pay']['order_id']
		order = Order.objects.get(id=int(order_id))
		store = order.store
		store_name = order.store.name
		if store.merchant != None:
			MERCHANT = store.merchant
		t_status = request.GET.get('Status')
		t_authority = request.GET['Authority']
		if request.GET.get('Status') == 'OK':
			req_header = {"accept": "application/json",
						  "content-type": "application/json'"}
			req_data = {
				"merchant_id": MERCHANT,
				"amount": order.get_final_payment()*10,
				"authority": t_authority
			}
			req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
			if len(req.json()['errors']) == 0:
				t_status = req.json()['data']['code']
				if t_status == 100:
					order.status = paid_status
					customer = order.customer
					if order.get_final_payment() >= customer.wallet_balance:
						customer.wallet_balance = 0
						order.paid_by_wallet = customer.wallet_balance
						
					else:
						customer.wallet_balance -= order.get_final_payment()
						order.paid_by_wallet = order.get_final_payment()
					customer.save()
					
					order.save()
					
					return render(request, self.template_name, {'message':'پرداخت شما موفقیت آمیز بود. سفارش شما ثبت گردید و در حال پردازش است ', 'ref_id':req.json()['data']['ref_id'], 'store_name':store_name})
				elif t_status == 101:
					return render(request, self.template_name, {'message':str(req.json()['data']['message']), 'store_name':store_name})
				else:
					return render(request, self.template_name, {'message':'پرداخت ناموفق ', 'store_name':store_name})
			else:
				e_code = req.json()['errors']['code']
				e_message = req.json()['errors']['message']
				return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
		else:
			return render(request, self.template_name, {'message':'پرداخت ناموفق ', 'store_name':store_name})










