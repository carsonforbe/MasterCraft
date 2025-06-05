from django.db import models

# Create your models here.
class Payment(models.Model):
    status = [
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('completed', 'Completed'),
    ]

    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    gateaway_reference = models.CharField(max_length=255, blank=True)