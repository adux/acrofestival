from django.db import models
# Create your models here.

Status = [
    ('IN','Informed'),
    ('CA','Canceled'),
    ('PA','Paid'),
    ('PE','Pending'),
    ('SW','Switched'),
    ('WL','Waiting List')
]

class Fest(models.Model):
    name        = models.CharField(max_length=120)
    address     = models.CharField(max_length=250)
    numero      = models.CharField(max_length=20)
    email       = models.CharField(max_length=250)
    option      = models.CharField(max_length=5)
    allergies   = models.CharField(max_length=300)
    amount      = models.CharField(max_length=10,null=True, blank=True)
    pay_till    = models.DateField(auto_now_add=False,auto_now=False, null=True, blank=True)
    pay_date    = models.DateField(auto_now_add=False,auto_now=False, null=True, blank=True)
    notes       = models.TextField(max_length=1000, null=True, blank=True)
    status      = models.CharField(max_length=15, choices=Status, default='PE', null=True, blank=True)
    date        = models.DateField(auto_now_add=True)
    datetime    = models.DateTimeField(auto_now_add=True)
    update      = models.DateField(auto_now=True)

