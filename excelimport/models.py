from django.db import models

# Create your models here.

class ExcelData(models.Model):
    data = models.JSONField(null=True, blank=True)

class Member(models.Model):

    name = models.CharField(max_length=100)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return self.name
    
