from django.db import models

# Create your models here.
Status = [
    ("IN", "Informed"),
    ("CA", "Canceled"),
    ("PA", "Paid"),
    ("PE", "Pending"),
    ("SW", "Switched"),
    ("WL", "Waiting List"),
]


class UrbanAcroBooking(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    option = models.CharField(max_length=20, null=True, blank=True)
    comment = models.CharField(max_length=300, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=Status, null=True, blank=True)
    pay_till = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    note = models.CharField(max_length=1000, null=True, blank=True)


class WinterAcroBooking(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=250)
    option = models.CharField(max_length=5)
    allergies = models.CharField(max_length=300)
    donation = models.CharField(max_length=3)
    amount = models.CharField(max_length=10, null=True, blank=True)
    pay_till = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    pay_date = models.DateField(
        auto_now_add=False, auto_now=False, null=True, blank=True
    )
    notes = models.TextField(max_length=1000, null=True, blank=True)
    status = models.CharField(
        max_length=15, choices=Status, default="PE", null=True, blank=True
    )
    date = models.DateField(auto_now_add=True)
    datetime = models.DateTimeField(auto_now_add=True)
    update = models.DateField(auto_now=True)
