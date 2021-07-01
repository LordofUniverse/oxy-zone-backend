from django.db import models
from django.db.models.fields.related import ForeignKey

class Sellers(models.Model):
    name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    profilephoto = models.ImageField(upload_to='media/', default = 'default.png')
    desc = models.TextField(default='')

    def _str_(self):
        return self.name

class Places(models.Model):
    foreign_seller = models.ForeignKey(Sellers, on_delete=models.CASCADE, null = False)
    location = models.TextField()
    addr = models.TextField()
    phno = models.BigIntegerField()
    oxyprice = models.FloatField()

    def _str_(self):
        return self.location
