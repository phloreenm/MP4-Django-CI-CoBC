from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'has_digital_file', 'created_at', 'updated_at')

    def has_digital_file(self, obj):
        return "Yes" if obj.digital_file else "No"
    has_digital_file.short_description = "Digital File Available"