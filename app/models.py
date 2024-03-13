from django.db import models
from django.contrib.auth.models import User
#from django.core.validators import MaxValueValidator, MinValueValidator

DIVISION_CHOICE = (
    ('Dhaka', 'Dhaka'),
    ('Khulna', 'khulna'),
    ('Rangpur', 'Rangpur'),
    ('Chottogram', 'Chottogram'),
    ('Cumilla', 'Cumilla'),
    ('Rajshahi', 'Rajshahi'),
    ('Sylhet', 'Sylhet'),
    ('Borishal', 'Borishal'),
)
class Customer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    division = models.CharField(choices=DIVISION_CHOICE, max_length=50)


    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES=(
    
     ('Top Wear Male','Top War Male'),
     ('Top Wear Female','Top War Female'),
 )

SIZE_CHOICES=(
     ('XS','XS'),
     ('S','S'),
     ('M','M'),
     ('L','L'),
     ('XL','XL'),
     ('XXL','XXL'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    size = models.CharField(choices=SIZE_CHOICES,max_length=3)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=15)
    product_image = models.ImageField(upload_to='produtcimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price