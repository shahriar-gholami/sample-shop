from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    store = serializers.CharField(max_length = 255)
    category_1 = serializers.CharField(max_length = 255)
    category_2 = serializers.CharField(max_length = 255)
    title = serializers.CharField(max_length = 255)
    description = serializers.CharField(max_length = 100000)
    features = serializers.ListField(allow_empty = True)
    brand = serializers.CharField(allow_null = True, allow_blank = True)
    price =  serializers.IntegerField()
    tags = serializers.ListField(allow_empty = True)
    images = serializers.ListField(allow_empty = True)



