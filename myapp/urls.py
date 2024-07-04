from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    path('add-student', views.add_student , name='add-student'),
    path('delete-student/<str:slug>/', views.delete_student, name='delete-student'),
    path('student-view/<str:slug>/', views.view_student, name='student-view'),
    path('update-student/<str:slug>/', views.update_student, name='update-student'),
    
    
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('logout', views.logout_user, name='logout')
]
