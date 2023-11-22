from django.db import models
from django.contrib.auth.models import User,UserManager
# Create your models here.





class Product(models.Model):
     owner=models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
     name = models.CharField(max_length=50)
     description = models.TextField(max_length=250, blank=True, null=True)
     price = models.DecimalField(default=0, decimal_places=2, max_digits=7)
     image = models.ImageField(upload_to='mystatic/img')


     def __str__(self):
          return self.name
     



    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f" {self.user} cart "

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super(CartItem, self).save(*args, **kwargs)

# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     cart_items = models.ForeignKey(CartItem, on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return  self.user
    



class Review(models.Model):
    rates= (
    (0,'0'),
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    description = models.TextField()
    rating = models.IntegerField(default=0, choices=rates)

    def __str__(self):
        return f"{self.product} = {self.rating}"






# class CartItem(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True )

#     def __str__(self):
#         return f"{self.product.name} x {self.quantity}"

# class Cart(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True, null=True )
#     cart_items = models.ForeignKey(CartItem, on_delete=models.CASCADE,blank=True, null=True)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return f"Cart {self.id}"