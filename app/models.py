from django.db import models

# Create your models here.

class ExcelData(models.Model):
    data = models.JSONField(null=True, blank=True)