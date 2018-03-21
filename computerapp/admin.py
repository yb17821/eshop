from django.contrib import admin

# Register your models here.


from .models import Product, Category, Manufacturer, DeliveryAddress, UserProfile, Order


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


admin.site.register(Category, CategoryAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


admin.site.register(Manufacturer, ManufacturerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'price', 'category', 'manufacturer', 'sold', ]
    list_editable = ['price', 'sold', 'category', ]


admin.site.register(Product, ProductAdmin)


class DeliveryaddressAdmin(admin.ModelAdmin):
    list_display = ["user", "contact_person", "contact_mobile_phone", "delivery_address"]


admin.site.register(DeliveryAddress, DeliveryaddressAdmin)


class UserprofileAdmin(admin.ModelAdmin):
    list_display = ["user", "mobile_phone", "nickname", "description", "icon", "delivery_address"]
    list_editable = ["delivery_address"]


admin.site.register(UserProfile, UserprofileAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "status", "user"]
    list_editable = ["status",]

admin.site.register(Order, OrderAdmin)
