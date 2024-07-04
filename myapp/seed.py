from .models import  RollNumber, Student
from faker import Faker
fake = Faker()

def seed_db():
    for _ in range(10):
        roll_number = RollNumber.objects.create(roll_number = fake.random_int(min=1000, max=9999))
        student = Student.objects.create(
            roll_number = roll_number,
            student_name = fake.name(),
            student_age = fake.random_int(min=10, max=20),
            student_class = fake.random_element(elements=('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')),
            student_section = fake.random_element(elements=('A', 'B', 'C', 'D', 'E')),
            student_image = fake.image_url()
        )
        student.save()
        roll_number.save()