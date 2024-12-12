from django.apps import AppConfig

class ShopConfig(AppConfig):
    name = 'shop'
    verbose_name = 'مدیریت فروشگاه'

    def ready(self):
        import shop.signals


