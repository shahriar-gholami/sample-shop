from urllib.parse import urlparse
from .models import Category, Store, Owner
from django.contrib.auth.models import AnonymousUser
from shop.models import Cart, Tag, Customer


store = Store.objects.all().first()
store_name = store.name



def base_template_context(request):

	for key, value in request.session.items():
		print (f'{key}:{value}')

	user_info = {}
	if request.user.is_authenticated:
		user_info = {
			'username': request.user.phone_number,
		}
	
	categories = None
	
	current_path = request.path
	parsed_url = urlparse(current_path)
	path_segments = parsed_url.path.split('/')
	second_segment = path_segments[1] if len(path_segments) > 2 else None
	third_segment = path_segments[2] if len(path_segments) > 3 else None
	special_tags = Tag.objects.filter(is_special = True)
	
	
	
	
		
	if 'temp_cat' in request.session:
		if request.session['temp_cat']:
			temp_category = Category.objects.get(name = request.session['temp_cat'])

			if 'category' in path_segments and temp_category.slug not in path_segments:
				for key in list(request.session.keys()):
					# بررسی آیا کلید با الگوی مورد نظر شروع می‌شود
					if key.startswith('filter-'):
						# پاک کردن کلید مربوطه
						del request.session[key]
						
						request.session.modified = True
				del request.session['temp_cat']
				
			if 'products' not in path_segments:
				for key in list(request.session.keys()):
					# بررسی آیا کلید با الگوی مورد نظر شروع می‌شود
					if key.startswith('filter-'):
						# پاک کردن کلید مربوطه
						del request.session[key]
						
						request.session.modified = True
				del request.session['temp_cat']

			if path_segments[-2] == 'products':
				for key in list(request.session.keys()):
					# بررسی آیا کلید با الگوی مورد نظر شروع می‌شود
					if key.startswith('filter-'):
						# پاک کردن کلید مربوطه
						del request.session[key]
						
						request.session.modified = True
				del request.session['temp_cat']


	top_categories = Category.objects.all()
	app_name = path_segments[1]
	if isinstance(request.user, AnonymousUser):
		from shop.models import Product
		from shop.models import Variety
		varieties = Variety.objects.all()
		products_id_list = []
		i = 0
		for variety in varieties:
			products_id_list.append(str(variety.id))
		for key, value in request.session.items():
			if key in products_id_list:
				i = i+1
		cart_url = f'shop:customer_authentication'
		account_url = f'shop:customer_authentication'
		return {
				'current_path': current_path,
				'second_segment': second_segment,
				'store_name':third_segment,
				'top_categories':top_categories,
				'cart_url':cart_url,
				'cart_items_count':i,
				'account_url':account_url,
				'store':store,
				'store_name':store_name,
				'special_tags':special_tags
			}
	else:
		top_categories = Category.objects.all()
		customer, create = Customer.objects.get_or_create(phone_number=request.user.phone_number)
		cart, create = Cart.objects.get_or_create(customer=customer)
		cart_items_count = cart.items.all().count()
		cart_url = f"'shop:cart_view' {cart.id}"
		owner = Owner.objects.filter(phone_number = request.user.phone_number).first()
		if owner != None:
			account_url = 'shop:owner_dashboard'
		else:
			account_url = 'shop:customer_dashboard'
		return {
				'user_info': user_info,
				'current_path': current_path,
				'second_segment': second_segment,
				'store_name':third_segment,
				'top_categories':top_categories,
				'cart_url':cart_url,
				'cart':cart,
				'cart_items_count':cart_items_count,
				'account_url':account_url,
				'store':store,
				'store_name':store_name,
				'special_tags':special_tags
			}        
