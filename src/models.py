from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



class User(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    username = models.CharField(null=True, max_length=200, unique=True)
    ninNo = models.IntegerField(null=True)
    name = models.CharField(max_length=200, null=True)
    phoneNo = models.IntegerField(null=True)
    address = models.TextField(null=True)
    state = models.CharField(max_length=200, null=True)
    lga = models.CharField(max_length=200, null=True)
    nextOfKin = models.CharField(max_length=200, null=True)
    nokAddress = models.TextField(null=True)
    nokPhoneNo = models.IntegerField(null=True)
    occupation = models.CharField(max_length=200, null=True)
    volunteerStatus = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=500)
    content = models.TextField(null=True)
    image1 = models.CharField(max_length=500, default=" ")
    image2 = models.CharField(max_length=500, default=" ")
    image3 = models.CharField(max_length=500, default=" ")
    audio = models.CharField(max_length=500, default=" ")
    video = models.CharField(max_length=500, default=" ")
    latitude = models.DecimalField(max_digits=25, decimal_places=20, null=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, null=True)
    created = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)


    def __str__(self):
        return self.category

    class Meta:
        ordering = ('-created',)

class Official(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=500)
    area = models.CharField(max_length=200)


    def __str__(self):
        return self.user.username



class Notification(models.Model):
    department = models.CharField(max_length=1000)
    state = models.CharField(max_length=200)
    lga = models.CharField(max_length=200)
    title = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created',)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=200)

    def __str__(self):
        return self.contact_person


class SafeTripReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Contact, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=25, decimal_places=20, null=True)
    longitude = models.DecimalField(max_digits=25, decimal_places=20, null=True)

    def __str__(self):
        return self.user