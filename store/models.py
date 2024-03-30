from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("store:category", kwargs={
            'slug': self.slug
        })

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', null=True, blank=True, default='products/default.jpg')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_price(self):
        return self.discount_price if self.discount_price else self.price

    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })


class CartProduct(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_true_price(self):
        return self.quantity * self.product.price

    def get_discount_price(self):
        return self.quantity * self.product.discount_price

    def get_amount_saved(self):
        return self.get_true_price() - self.get_discount_price()

    def get_price(self):
        if self.product.discount_price:
            return self.get_discount_price()
        return self.get_true_price()


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    session_key = models.CharField(max_length=40, null=True)
    products = models.ManyToManyField(Product, through='CartProduct')
    date_created = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        total = 0
        for order_item in self.cartproduct_set.all():
            total += order_item.get_price()
        return total


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)

    placed = models.BooleanField(default=False)
    time_placed = models.DateTimeField(null=True, blank=True)

    sent_out = models.BooleanField(default=False)
    time_sent = models.DateTimeField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
