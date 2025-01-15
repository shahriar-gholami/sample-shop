from django.contrib.auth.mixins import UserPassesTestMixin
from urllib.parse import urlparse
from .models import Store, Owner, Customer





class IsOwnerUserMixin(UserPassesTestMixin):
	# store_name = Store.objects.all().first().name
	# store = Store.objects.all().first()
	def test_func(self):
		if self.request.user.is_authenticated:
			current_path = self.request.path
			parsed_url = urlparse(current_path)
			path_segments = parsed_url.path.split('/')
			store_name = path_segments[2]
			owner = Owner.objects.filter(phone_number = self.request.user.phone_number).first()
			if owner != None:
				return True
			return False
		return False
	
class IsCustomerUserMixin(UserPassesTestMixin):
	# store_name = Store.objects.all().first().name
	# store = Store.objects.all().first()
	def test_func(self):
		if self.request.user.is_authenticated:
			current_path = self.request.path
			parsed_url = urlparse(current_path)
			customer = Customer.objects.filter(phone_number = self.request.user.phone_number).first()
			if customer != None:
				return True
			return False
		return False
