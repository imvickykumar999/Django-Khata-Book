from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, related_name='purchases', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_payment = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item_name} - {self.customer.name}"
