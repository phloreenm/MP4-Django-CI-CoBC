from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'city', 'country')
    search_fields = (
        'user__username', 
        'user__email', 
        'user__first_name', 
        'user__last_name', 
        'phone_number', 
        'city'
    )

    def first_name(self, obj):
            return obj.user.first_name
            first_name.admin_order_field = 'user__first_name'
            first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.user.last_name
    last_name.admin_order_field = 'user__last_name'
    last_name.short_description = 'Last Name'

admin.site.register(Profile, ProfileAdmin)