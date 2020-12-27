from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class PUResult(models.Model):
    pu_roll = models.CharField(max_length=6, default='909090', primary_key=True)
    marks = models.IntegerField(('marks'), validators=[MinValueValidator(0), MaxValueValidator(300)])
    year = models.IntegerField(('year'), validators=[MinValueValidator(2018), MaxValueValidator(2020)])

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    pu_roll = models.OneToOneField(PUResult, on_delete=models.CASCADE)
    ph_number = models.CharField(max_length=10, default = 'for existing')
    address = models.CharField(max_length=300, default = 'for existing')
    bc_number = models.CharField(max_length=10, default = 'for existing')
    adhaar_number = models.CharField(max_length=50, default = 'for existing')
    dob = models.DateField(default=datetime.date.today()) 

class PreviousDegree(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    college_id = models.CharField(max_length=50)
    usn = models.CharField(max_length=50)

class KCETResult(models.Model):
    rank = models.IntegerField(('rank'), default='1400', max_length=5, validators=[MinValueValidator(1), MaxValueValidator(1400)], primary_key=True)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    marks = models.IntegerField(('year'), validators=[MinValueValidator(0), MaxValueValidator(180)])

class FormLastActive(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

class DocumentVerified(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_id = models.IntegerField(unique=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    verified = models.BooleanField()