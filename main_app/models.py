from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Power(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('power_detail', kwargs={'pk': self.id})

class Superhero(models.Model):  # Note that parens are optional if not inheriting from another class
    name = models.CharField(max_length=100)
    power = models.CharField(max_length=100)    
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    add_powers = models.ManyToManyField(Power)

    	
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'superhero_id': self.id})