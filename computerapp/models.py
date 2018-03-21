from django.db import models

# Create your models here.


from django.conf import settings


class Category(models.Model):
    """
    商品类别：笔记本、平板电脑、一体机、台式机、服务器
    """  
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Manufacturer(models.Model):
    """
    生产厂商
    """  
    name = models.CharField(max_length=200)
    description = models.TextField()    
    logo = models.ImageField(blank=True, null=True, max_length=200, upload_to='manufacturer/uploads/%Y/%m/%d/')            
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name






class Product(models.Model):
    """
    产品
    """  
    model = models.CharField(max_length=200)
    description = models.TextField()  
    image = models.ImageField(max_length=200, upload_to='product/uploads/%Y/%m/%d/')        
    price = models.DecimalField(max_digits=12, decimal_places=2)
    sold = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, related_name='product_in', on_delete=models.DO_NOTHING)
    manufacturer = models.ForeignKey(Manufacturer, related_name='product_of', on_delete=models.DO_NOTHING)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model







class DeliveryAddress(models.Model):
    """
    收货地址
    """  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='delivery_address_of',)
    contact_person = models.CharField(max_length=200)
    contact_mobile_phone = models.CharField(max_length=200)
    delivery_address = models.TextField()  
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.delivery_address







class UserProfile(models.Model):
    """
    用户信息
    """  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='profile_of',)
    mobile_phone = models.CharField(blank=True, null=True, max_length=200)
    nickname = models.CharField(blank=True, null=True, max_length=200)
    description = models.TextField(blank=True, null=True)  
    icon = models.ImageField(blank=True, null=True, max_length=200, upload_to='user/uploads/%Y/%m/%d/')        
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    delivery_address = models.ForeignKey(DeliveryAddress, related_name='user_delivery_address', on_delete=models.DO_NOTHING, blank=True, null=True,)


class Order(models.Model):
    STATUS_CHOICES =(
        ("0","new"),
        ("1", "not paid"),
        ("2", "paid"),
        ("3", "transport"),
        ("4", "closed"),
    )
    status = models.CharField(choices=STATUS_CHOICES,default="0",max_length=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='order_of', )
    product = models.ForeignKey(Product,related_name="order_product",on_delete=models.DO_NOTHING,)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    remark = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    address = models.ForeignKey(DeliveryAddress,related_name="order_address",on_delete=models.DO_NOTHING,)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "order of %d" % (self.user.id)
































