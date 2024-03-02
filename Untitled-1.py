# bookings/models.py
from django.db import models

class MassageType(models.Model):
    name = models.CharField(max_length=50)

class Booking(models.Model):
    massage_type = models.ForeignKey(MassageType, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
python manage.py makemigrations
python manage.py migrate
# bookings/views.py
from django.shortcuts import render, redirect
from .models import MassageType, Booking
from django.utils import timezone

def index(request):
    bookings = Booking.objects.filter(date_time__gte=timezone.now()).order_by('date_time')
    return render(request, 'bookings/index.html', {'bookings': bookings})

def make_booking(request):
    if request.method == 'POST':
        massage_type_id = request.POST['massage_type']
        date_time = request.POST['date_time']
        massage_type = MassageType.objects.get(pk=massage_type_id)
        Booking.objects.create(massage_type=massage_type, date_time=date_time)
        return redirect('index')
    massage_types = MassageType.objects.all()
    return render(request, 'bookings/make_booking.html', {'massage_types': massage_types})
# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('make_booking/', views.make_booking, name='make_booking'),
]
# massage_booking/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),
]
<!-- bookings/templates/bookings/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Massage Bookings</title>
</head>
<body>
    <h1>Upcoming Massage Bookings</h1>
    <ul>
        {% for booking in bookings %}
            <li>{{ booking.massage_type.name }} - {{ booking.date_time }}</li>
        {% endfor %}
    </ul>
    <a href="{% url 'make_booking' %}">Make a Massage Booking</a>
</body>
</html>
<!-- bookings/templates/bookings/make_booking.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Make a Massage Booking</title>
</head>
<body>
    <h1>Make a Massage Booking</h1>
    <form method="post" action="{% url 'make_booking' %}">
        {% csrf_token %}
        <label for="massage_type">Select Massage Type:</label>
        <select name="massage_type" required>
            {% for massage_type in massage_types %}
                <option value="{{ massage_type.id }}">{{ massage_type.name }}</option>
            {% endfor %}
        </select><br>
        <label for="date_time">Date and Time:</label>
        <input type="datetime-local" name="date_time" required><br>
        <button type="submit">Submit</button>
    </form>
    <a href="{% url 'index' %}">Back to Massage Bookings</a>
</body>
</html>
python manage.py runserver
