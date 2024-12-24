from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Conversion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    input_format = models.CharField(max_length=10)
    output_format = models.CharField(max_length=10)
    input_file_url = models.URLField()
    output_file_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.TextField()

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
