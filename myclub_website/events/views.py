from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Fabian"
    month = month.capitalize()
    #Convertir meses de nombres a numeros
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    #Crear un calendario
    cal = HTMLCalendar().formatmonth(year, month_number)
    #Obtener year actual
    now = datetime.now()
    current_year = now.year
    #Obtener hora actual
    time = now.strftime('%I:%M %p')    
    return render(request, 
        'events/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_year": current_year,
        "time": time,
    })
