from django.db import models
# Create your models here.
class Booking(models.Model):
    Status = (
        ('IN','Informed'),
        ('CA','Canceled'),
        ('PA','Payed'),
        ('PE','Pending'),
        ('SW','Switched')
    )
    name            = models.CharField(max_length=120)
    address         = models.CharField(max_length=120)
    numero          = models.CharField(max_length=30)
    email           = models.CharField(max_length=50)
    option          = models.CharField(max_length=20, null=True, blank=True)
    comment         = models.CharField(max_length=300, null=True, blank=True)
    date            = models.DateField(auto_now_add=True)
    datetime        = models.DateTimeField(auto_now_add=True)
    status          = models.CharField(max_length=15, choices=Status, null=True, blank=True)
    pay_till        = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    note            = models.CharField(max_length=1000, null=True, blank=True)
