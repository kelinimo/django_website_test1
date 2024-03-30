from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class UserProfile(models.Model):
#     user: User = models.OneToOneField(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
#     one_click_purchasing = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.user.username

