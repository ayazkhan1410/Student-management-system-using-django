from django.contrib import admin
from .models import (CustomUser, Contact, Student, RollNumber)
# Register your models here.
@admin.register(CustomUser)
class AdminUser(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'user_profile', )
    list_per_page = 10
    search_fields = ['first_name', 'email']
    
@admin.register(RollNumber)
class AdminRollNumber(admin.ModelAdmin):
    list_display = ['roll_number']
    search_fields = ['roll_number']
    ordering = ['roll_number']
@admin.register(Student)
class AdminStudent(admin.ModelAdmin):
    list_display = ['roll_number', 'student_name', 'student_age', 'student_class', 'student_section', 'student_image']
    search_fields = ['student_name', 'student_class']
    list_filter = ['student_name', 'student_class']
    ordering = ['student_name']
    list_per_page = 10
    
@admin.register(Contact)
class AdminContact(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'message']
    search_fields = ['name', 'email']
    list_filter = ['name', 'email']
