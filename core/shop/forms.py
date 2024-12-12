
from django import forms
from django.utils import timezone
from django.forms import modelformset_factory
from .models import Store, Slide, Delivery, Category, ProductImage, Comment, Product, Variety, Coupon, OrderStatus, Size
from ckeditor.widgets import CKEditorWidget
from django.core import validators


class NewSiteForm(forms.Form):
    site_name = forms.CharField(max_length=100, label='Site Name', required=False)
    recommender = forms.CharField(max_length=6, required=False)
    store_field = forms.CharField()

class OwnerForm(forms.Form):
    full_name = forms.CharField(max_length=250)
    phone_number = forms.CharField(max_length=11)

class VerifyOwnerForm(forms.Form):
    code = forms.CharField(max_length=6)

class AuthenticationCodeForm(forms.Form):
    code = forms.IntegerField()

class OwnerLoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)

class StoreForm(forms.Form):
    country = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    city = forms.CharField(required=False)
    instagram = forms.CharField(required=False)
    address = forms.CharField(required=False)
    about = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)

class IndexTitleUpdateForm(forms.Form):
    index_title = forms.CharField(required=False)

class EnamadUpdateForm(forms.Form):
    enamad = forms.CharField(required=False)

class DeliveryForm(forms.Form):
    name =forms.CharField(max_length=250, required=False)
    price = forms.IntegerField()

class TagForm(forms.Form):
    name =forms.CharField(max_length=250, required=False)
    slug = forms.CharField(max_length=250, required=False)
    is_special = forms.BooleanField(required=False)

class CategoryForm(forms.Form):
    name = forms.CharField(max_length=250)
    is_sub = forms.BooleanField(required=False)
    parent = forms.CharField()
   
class ProductImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.ClearableFileInput())

    class Meta:
        model = ProductImage
        fields = ['alt_name',]

class CommentForm(forms.Form):
    email = forms.EmailField()
    body = forms.CharField()

class ProductForm(forms.Form):
        
        name = forms.CharField(max_length=250,required=False)
        description = forms.CharField(widget=CKEditorWidget(), required=False)
        tags = forms.CharField(max_length=1000, required=False)
        features = forms.CharField(max_length=1000, required=False)
        color = forms.CharField(max_length=250, required=False)
        brand = forms.CharField(max_length=250, required=False)
        price = forms.IntegerField(required=False)
        sales_price = forms.IntegerField(required=False)
        off_active = forms.CharField(max_length=250, required=False)
        is_original = forms.CharField(max_length=250, required=False)
        category = forms.CharField(max_length=250, required=False)

class EditFilterTitleForm(forms.Form):
    name = forms.CharField()
        
class FilterProductsForm(forms.Form):
    category = forms.CharField(required=False)
    # size = forms.MultipleChoiceField(
    #     choices = [(size.id, size.name) for size in Size.objects.all()],
    #     widget=forms.SelectMultiple(attrs={'class': 'filter-multi'},),
    #     required=False
    # )
    price_range = forms.CharField(required=False)
    brand = forms.CharField(required=False)
    color = forms.CharField(required=False)

class CartEditForm(forms.Form):
    count = forms.IntegerField()

class PurchaseForm(forms.Form):
    size = forms.CharField(required=False)
    count = forms.IntegerField()

class VarietyForm(forms.ModelForm):
    class Meta:
        model = Variety
        fields = ['name', 'stock',]

class VarietyUpdateForm(forms.Form):
    stock = forms.IntegerField()

class RequestNumberForm(forms.Form):
    phone_number = forms.CharField(max_length=11, validators=[validators.RegexValidator(r'^\d{11}$', 'شماره تلفن باید 11 رقمی و بدون حروف باشد.')])

class CouponApplyForm(forms.Form):
	code = forms.CharField()

class DeliveryApplyForm(forms.Form):
	delivery = forms.CharField()

class CouponForm(forms.Form):
    code = forms.CharField()
    discount = forms.IntegerField()
    from_time = forms.CharField()
    to_time = forms.CharField()

class OrderStatusForm(forms.Form):
    order_status = forms.ModelChoiceField(queryset=OrderStatus.objects.all(), empty_label=None)

class ContactUsForm(forms.Form):
    name = forms.CharField()
    familly_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    subject = forms.CharField()
    message_text = forms.CharField(widget=CKEditorWidget())

class HomePageUpdateForm(forms.ModelForm):

    image = forms.ImageField(widget=forms.ClearableFileInput())

    class Meta:
        model = Slide
        fields = ['alt_name',]

class AddSlideForm(forms.Form):

    image = forms.ImageField(widget=forms.ClearableFileInput(), required=False)
    source = forms.CharField(required=False)
    alt_name = forms.CharField(required=False)

class AddBannerForm(forms.Form):

    image = forms.ImageField(widget=forms.ClearableFileInput(), required=False)
    source = forms.CharField(required=False)
    alt_name = forms.CharField(required=False)

class FaqForm(forms.Form):
    question = forms.CharField()
    answer = forms.CharField()

class CustomerForm(forms.Form):
      full_name = forms.CharField()
      email = forms.EmailField()
      city = forms.CharField()
      zip_code = forms.CharField()
      address = forms.CharField()

class LogoUpdateForm(forms.Form):
    logo = forms.ImageField(widget=forms.ClearableFileInput(), required=False)

class WithdrawForm(forms.Form):
    sheba_number = forms.CharField()
    amount = forms.IntegerField()

class BlogPostCreateForm(forms.Form):
    title = forms.CharField()
    body = forms.CharField(widget=CKEditorWidget())
    published = forms.BooleanField(required=False)
    category = forms.CharField(required=False)
    

class BlogCategoryForm(forms.Form):
    name = forms.CharField()

class PostThumbnailUpdateForm(forms.Form):
    thumbnail = forms.ImageField(widget=forms.ClearableFileInput(), required=False)

class ImageUploadForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput())

class HomeCategoryShowForm(forms.Form):
    categories = forms.MultipleChoiceField(
        choices = [(category.id, category.name) for category in Category.objects.all()],
        widget=forms.SelectMultiple(attrs={'class': 'filter-multi'},),
        required=False
    )

class SubscriptionForm(forms.Form):
    email = forms.EmailField()

class CheckoutForm(forms.Form):
    name = forms.CharField(required = False)
    familly_name = forms.CharField(required = False)
    phone_number = forms.CharField(required = False)
    email = forms.EmailField(required = False)
    state = forms.CharField(required = False)
    city = forms.CharField(required = False)
    zip_code = forms.CharField(required = False)
    address = forms.CharField(required = False)

class ThemeForm(forms.Form):
    layout = forms.CharField(required=False)
    color = forms.CharField(required=False)

class MetaForm(forms.Form):
    meta_description = forms.CharField(required=False)
    meta_keywords = forms.CharField(required=False)
    meta_og_title = forms.CharField(required=False)
    meta_og_description = forms.CharField(required=False)
    meta_tc_title = forms.CharField(required=False)
    meta_tc_description = forms.CharField(required=False)

class TicketForm(forms.Form):
    subject = forms.CharField(required=True)
    body = forms.CharField()

class TicketReplyForm(forms.Form):
    body = forms.CharField(required = True)

class PoliciesForm(forms.Form):
    policies = forms.CharField(widget=CKEditorWidget(), required=False)

class AddFilterForm(forms.Form):
    category = forms.CharField()
    name = forms.CharField()

class AsignFilterToProductForm(forms.Form):
    filter = forms.CharField()
    value = forms.CharField()

class FeatureFilterForm(forms.Form):
    def __init__(self, choices):
        self.choices = choices
        self.options = forms.MultipleChoiceField(choices=choices, widget=forms.CheckboxSelectMultiple)
    
class AddingProductFromDigiForm(forms.Form):
    dkp_code = forms.CharField()
    category = forms.CharField()

class CategorySelectForm(forms.Form):
    category_select = forms.CharField()

class MerchantCodeForm(forms.Form):
    merchant_code = forms.CharField()

class RecieverDetailsForm(forms.Form):
    name = forms.CharField(required = False)
    familly_name = forms.CharField(required = False)
    phone_number = forms.CharField(required = False)
    email = forms.EmailField(required = False)
    state = forms.CharField(required = False)
    city = forms.CharField(required = False)
    zip_code = forms.CharField(required = False)
    address = forms.CharField(required = False)

class OrderDeliveryOptionsForm(forms.Form):
    express_time_express = forms.CharField(required=False)
    express_day_normal = forms.CharField(required=False)
    express_time_normal = forms.CharField(required=False)
    normal_day = forms.CharField(required=False)
    normal_time = forms.CharField(required=False)






    