from django.db import models
from django.contrib.auth.models import Permission, User

class Companie(models.Model):
    user = models.ForeignKey(User, default=1)
    companie_name = models.CharField(max_length=250)
    address = models.CharField(max_length=500)
    companie_logo = models.FileField()

    def __str__(self):
        return self.companie_name

class Employee(models.Model):
    companie = models.ForeignKey(Companie, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=250)
    employee_surname = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.employee_name + ' ' + self.employee_surname