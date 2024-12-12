from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.utils import timezone
from django.core.files.base import ContentFile
from .serializers import ProductSerializer
from shop.models import Store, Product, Category, ProductImage, Variety, Brand, Feature, Tag

features_list = []

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
            image_name = f'{product.name}-{store.name}'
            timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"{timestamp}_{image_name}"
            
            image = ProductImage(
                store=store,
                product=product,
            )
            
            image.image.save(image_filename, ContentFile(response.content))
            image.save()

class ProductListCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            store = Store.objects.get(name = serializer.data['store'])
            category_1, create = Category.objects.get_or_create(store=store, name = serializer.data['category_1'])
            if create:
                category_1.slug = category_1.name.replace(' ','-')
                category_1.save()
            category_2, create = Category.objects.get_or_create(store=store, name = serializer.data['category_2'])
            if create:
                category_2.slug = category_2.name.replace(' ','-')
                category_2.save()
            if category_1 != None and category_2 != None:
                category_2.parent = category_1
                category_2.is_sub = True
                category_2.save()
            title = serializer.data['title']
            slug = title.replace(' ','-')
            description = serializer.data['description']
            features = serializer.data['features']
            brand = serializer.data['brand']
            product_brand, create = Brand.objects.get_or_create(
                name = brand,
                store = store
            )
            price = serializer.data['price']
            tags = serializer.data['tags']
            new_product = Product.objects.create(
                name = title,
                store = store,
                slug = slug,
                description = description,
                features = format_features(features),
                brand = product_brand.name,
                price = price,
            )
            new_product.category.add(category_1)
            new_product.category.add(category_2)
            new_product.save()
            images = serializer.data['images']
            download_and_save_images(images, new_product.id)

            default_variety = Variety.objects.create(
				store = store,
				name = 'default variety',
				product = new_product, 
				stock = 2,
			)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CorrectProductSlugs(APIView):
    def post(self, request):
        # تعداد محصولات اصلاح شده
        corrected_count = 0
        
        products = Product.objects.all()
        for product in products:
            if '/' in product.slug:  # بررسی اینکه آیا نیاز به اصلاح دارد
                product.slug = product.slug.replace('/', '')
                product.save()
                corrected_count += 1
        
        # بازگشت پاسخ مناسب
        return Response(
            {
                "message": f"Successfully corrected slugs for {corrected_count} products.",
                "total_products": products.count(),
                "corrected_products": corrected_count,
            },
            status=status.HTTP_200_OK
        )
        






