from django.db import models

# Create your models here.

class Hospital(models.Model):
    name = models.CharField(default='unnamed')
    address = models.CharField(default='nema')
class Equipment(models.Model):
    equipment_id = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

class Contract(models.Model):
    hospital = models.ForeignKey(Hospital, related_name='hospital', on_delete=models.CASCADE, default=0)
    date = models.DateTimeField(default='2024-01-01 00:00:00')
    company = models.IntegerField(default=-1)
    equipment = models.ManyToManyField(Equipment)

