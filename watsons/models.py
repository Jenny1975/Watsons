from django.db import models
from django.contrib.auth.models import User
import time
import datetime



# Create your models here.

class Customer(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    gender_choice = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
    customer_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=1, choices = gender_choice, default = MALE)
    birthday = models.DateField(blank=True, null=True)
    marketing_spending = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.customer_name

        


class Product(models.Model):
    COSMETIC = 'CO'
    SNACK = 'SA'
    CARE_PRODUCT = 'CR'
    Facial_Cleanser = 'FC'
    Makeup_Remover = 'MR'
    Lotion = 'LO'
    Mask = 'MA'
    Sunscreen_lotion = 'SL'
    Mouthwash = 'MW'
    Toothpaste = 'TP'

    category_choice = (
        (COSMETIC, 'Cosmetic'),
        (SNACK, 'Snacks'),
        (CARE_PRODUCT, 'Care Product'),
        (Facial_Cleanser, 'Facial Cleanser'),
        (Makeup_Remover, 'Makeup Remover'),
        (Lotion, 'Lotion'),
        (Mask, 'Mask'),
        (Sunscreen_lotion, 'Sunscreen lotion'),
        (Mouthwash, 'Mouthwash'),
        (Toothpaste, 'Toothpaste'),
    )
    product_id = models.TextField(default="100000000")
    product_name = models.CharField(max_length=30)
    category = models.CharField(max_length = 2, choices = category_choice, default = COSMETIC )
    price = models.PositiveIntegerField()
    brand = models.CharField(max_length = 100)  # could be a foreignkey ?
    quantity = models.IntegerField()
    quantity_safe = models.IntegerField(default = 1 )
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class Transaction(models.Model):
    transaction_total = models.IntegerField(blank=True, null=True)
    transaction_id = models.PositiveIntegerField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    time = models.DateField(blank=True, null=True)
    delta_date = models.IntegerField(blank=True, null=True)
    amount = models.IntegerField()

    @staticmethod
    def create_total(self):
        product_amount = self.amount
        product = self.product
        total_amount = product_amount*product.price
        return total_amount


    def time_delta(self):
        date_now = datetime.date.today()
        delta = date_now - self.time
        return delta.days

    def save(self):
        if self.transaction_total is None:
            self.transaction_total = Transaction.create_total(self)
        # if self.transaction_id is None:
        #     self.transaction_id = self.create_transaction_num(self)
        if self.delta_date is None:
            self.delta_date = Transaction.time_delta(self)
        super().save()



class Location(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location_name = models.CharField(max_length=10)

    def __str__(self):
        return self.location_name

class Bonus(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    period = models.DateTimeField(blank=True, null=True)

class Pocket_other(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_Cosmetic = models.IntegerField(default=0)
    total_Snacks = models.IntegerField(default=0)
    total_Care = models.IntegerField(default=0)

class Staff(models.Model):
    phone = models.CharField(max_length=50, null=True)
    isManager = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return User.objects.get(id=self.user_id).username


class Servive(models.Model):
    Num = models.IntegerField(default=0)
    Date = models.IntegerField(default=0)
    retentention_rate = 0
    servive_rate = 0
    respected_customer_num = 0
    customer_num = 0
    def count(self,r,s):
        self.retentention_rate = r
        self.servive_rate = self.retentention_rate * s
        self.customer_num = 100*self.servive_rate
        self.respected_customer_num = self.customer_num*self.Date





