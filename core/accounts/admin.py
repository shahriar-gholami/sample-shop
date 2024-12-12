from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # فیلدهایی که در لیست نمایش ادمین ظاهر می‌شوند
    list_display = ('phone_number', 'full_name', 'is_active', 'is_staff', 'is_superuser','is_customer')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    
    # فیلدهایی که در فرم ایجاد و ویرایش کاربر نمایش داده می‌شوند
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Roles', {'fields': ('is_customer', 'is_shopowner')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number', 'full_name')
    ordering = ('phone_number',)
    filter_horizontal = ()

# رجیستر کردن مدل و ادمین سفارشی
admin.site.register(User, UserAdmin)
