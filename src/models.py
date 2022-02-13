from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(null=True, unique=True)
    username = models.CharField(null=True, max_length=200, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
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
        return self.email



class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=500)
    content = models.TextField(null=True)
    image1 = models.ImageField(null=True, upload_to='images')
    image2 = models.ImageField(null=True, upload_to='images')
    image3 = models.ImageField(null=True, upload_to='images')
    audio = models.FileField(null=True, upload_to='audios')
    video = models.FileField(null=True, upload_to='videos')
    latitude = models.DecimalField(max_digits=20, decimal_places=20, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=20, null=True)
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