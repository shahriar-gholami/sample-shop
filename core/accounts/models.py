from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, phone_number, **extra_fields):

        if not phone_number:
            raise ValueError(_("the phone number must be set"))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password('88256989Aa!')
        user.save()
        return user

    def create_superuser(self, phone_number, **extra_fields):
  
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone_number, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length = 11, unique = True)
    full_name = models.CharField(max_length = 250, default = 'نام و نام خانوادگی')
    otp_token = models.IntegerField(null=True, blank= True)
    is_superuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)
    is_shopowner= models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.phone_number
    
class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created']

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'

    
