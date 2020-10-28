from django.db import models
from django.utils import timezone

# Create your models here.  
class Personal(models.Model):
    name = models.CharField(max_length=30, default="Levit Osei-Wusu")
    telephone = models.CharField(max_length=15)
    twitter = models.URLField()
    email = models.EmailField(default='lkanner21@gmail.com')
    github = models.URLField()
    
    
    def __str__(self):
        return self.name
    

class Language(models.Model):
    person = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="languages")
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name