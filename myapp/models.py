from django.db import models
from django.contrib.auth.models import AbstractUser
from .helpers import Manager
from django.utils.text import slugify

# Create your models here.
class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    user_profile = models.ImageField(upload_to='user_profile/', default='user_profile/default.webp')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = Manager()

    def __str__(self) -> str:
        return self.email

class RollNumber(models.Model):
    roll_number = models.CharField(max_length=10, unique=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.roll_number
    
class Student(models.Model):
    roll_number = models.ForeignKey(RollNumber, on_delete=models.CASCADE, related_name='student_roll_number', null=True,blank=True)
    student_name = models.CharField(max_length=100, null=True,blank=True)
    student_age = models.IntegerField(null=True,blank=True)
    student_class = models.CharField(max_length=10, null=True,blank=True)
    student_section = models.CharField(max_length=10, null=True,blank=True)
    student_image = models.ImageField(upload_to='student_image/')
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.student_name)
        super(Student, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.student_name
    
class Contact(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField()
    
    def __str__(self):
        return self.name