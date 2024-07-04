from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (CustomUser as User, Contact, Student, RollNumber)
from django.db.models import Q

# Create your views here.
@login_required(login_url='login')
def index(request):
    try: 
        students = Student.objects.all().order_by('-id')
        paginator = Paginator(students, 5)  
        page_number = request.GET.get('page')
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1  # Default to page 1 if page number is invalid
        student_obj = paginator.page(page_number)
    except PageNotAnInteger:
        student_obj = paginator.page(1)
    except EmptyPage:
        student_obj = paginator.page(paginator.num_pages)
    except Exception as e:
        print("Exception: ", e)
        student_obj = None
    
    if request.method == "POST":
        search = request.POST.get('search')
        if search:
            students = students.filter(
                Q(student_name__icontains=search)|
                Q(student_class__icontains=search) |
                Q(student_section__icontains=search)
            )
            paginator = Paginator(students, 5)
            page_number = request.GET.get('page')
            try:
                page_number = int(page_number)
            except (TypeError, ValueError):
                page_number = 1  
            student_obj = paginator.page(page_number)

    context = {
        'student_obj': student_obj
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def add_student(request):
    
    if request.method == "POST":
        student_name = request.POST.get('student_name')
        student_age = request.POST.get('student_age')
        student_class = request.POST.get('student_class')
        student_section = request.POST.get('student_section')
        roll_number_value = request.POST.get('roll_number')
        student_image = request.FILES.get('student_image')  

        roll_number, created = RollNumber.objects.get_or_create(roll_number=roll_number_value)

        student_obj = Student.objects.create(
            student_name=student_name,
            student_age=student_age,
            student_class=student_class,
            student_section=student_section,
            roll_number=roll_number,
            student_image=student_image,
        )
        
        student_obj.save()
        messages.success(request, 'Student Record saved successfully')
        return redirect('add-student')

    return render(request, 'add-student.html')

@login_required(login_url='login')
def update_student(request, slug):
    student_obj = get_object_or_404(Student, slug=slug)
    roll_numbers = RollNumber.objects.all()

    if request.method == "POST":
        student_name = request.POST.get('student_name')
        student_age = request.POST.get('student_age')
        student_class = request.POST.get('student_class')
        student_section = request.POST.get('student_section')
        roll_number_id = request.POST.get('roll_number')
        student_image = request.FILES.get('student_image')

        roll_number = get_object_or_404(RollNumber, id=roll_number_id)

        student_obj.student_name = student_name
        student_obj.student_age = student_age
        student_obj.student_class = student_class
        student_obj.student_section = student_section
        student_obj.roll_number = roll_number

        if student_image:
            student_obj.student_image = student_image

        student_obj.save()
        messages.success(request, 'Student record updated successfully')
        return redirect('student-view', slug=student_obj.slug)

    context = {
        'student_obj': student_obj,
        'roll_numbers': roll_numbers
    }
    return render(request, 'update-student.html', context)

@login_required(login_url='login')
def view_student(request, slug):
    
    try:
        student_view = get_object_or_404(Student, slug = slug)
      
        
    except Exception as e:
        print('Exception: ', e)
        
    context = {
        'student_view': student_view  
    }
    return render(request, 'student-view.html', context)

@login_required(login_url='login')
def delete_student(request, slug):
    student_obj = Student.objects.get(slug = slug)
    student_obj.delete()
    messages.success(request, 'Student deleted successfully')
    return redirect('/')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        user = authenticate(email = email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid Email and Password')
            return redirect('login')
       
    return render(request, 'login.html')

def signup(request):
    
    if request.method == "POST":
        name = request.POST.get('name')
        email =  request.POST.get('email')
        password = request.POST.get('password')
        
        speical_char = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=']
        
        if len(password) < 8 and not any(char in speical_char for char in password):
            messages.error(request, "Password must be atleast 8 characters and must contain special characters")
            return redirect('signup')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Account already exists")
            return redirect('signup')
        
        user = authenticate(email = email, password = password, first_name = name)
        if not user is None:
            messages.info(request, "invalid Email and Password")
            
        user_obj = User.objects.create(
            first_name = name,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        
        authenticated_user = authenticate(request, email=email, password=password)
        
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('/')
        
        messages.info(request, 'Account created successfully, please login')
        return redirect('login')
     
    return render(request, 'signup.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, 'Your message has been sent successfully. We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def logout_user(request):
    logout(request)
    return redirect('/')