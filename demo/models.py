from django.db import models

# Create your models here.
class Demo(models.Model):
    text = models.CharField(max_length=50)
    number = models.IntegerField()
    
    def __str__(self):
        return self.text