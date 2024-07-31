from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, FileResponse
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator



def venue_pdf(request):
	# Create Bytestream buffer
	buf = io.BytesIO()
	# Create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)

	venues = Venue.objects.all()

	# Create blank list
	lines = []

	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append(" ")

	# Loop
	for line in lines:
		textob.textLine(line)

	# Finish Up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	# Return something
	return FileResponse(buf, as_attachment=True, filename='venue.pdf')

    
#Generate csv File Venue List
def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    
    #Create a csv writer
    writer = csv.writer(response)

    # Designate the model
    venues = Venue.objects.all()
    
    #Add column headings to the csv file
    writer.writerow(['Venue Name','Address','Zip Code','Phone Number','Web Address','Email'])
    
    #Loop thu and output
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

    return response

#Generate Txt File Venue List
def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate the model
    venues = Venue.objects.all()
    #Create blank list
    lines = []
    #Loop thu and output
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.zip_code}\n{venue.phone}\n{venue.web}\n{venue.email_address}\n\n\n')
    
    #Write to TextFile
    response.writelines(lines)
    return response

#Delete an Event
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('list-events')

#Delete a Venue
def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')

#Function to add events
def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')
    else:
        form = EventForm
        if 'submitted' in request.GET:
            submitted=True
    return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted})

#Function to update an event, it gets the data and you can change with the EventForm
def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    #Instace uses to get all the data from the db
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html', {'event':event,
                                                        'form':form})

#Function to update a venue, it gets the data and you can change with the VenueForm
def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    #Instace uses to get all the data from the db
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue':venue,
                                                        'form':form})
#Function to search Venues on the navbar
def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched':searched, 'venues':venues})
    else:
        return render(request, 'events/search_venues.html', {'searched':searched})

def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    return render(request, 'events/show_venue.html', {'venue':venue})

def list_venues(request):
    venue_list = Venue.objects.all()
    #Set up Pagination
    p = Paginator(Venue.objects.all(), 1)#How many show per page
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages #Counter to know how many pages are
    return render(request, 'events/venue.html', {'venue_list':venue_list,
                                                 'venues':venues,
                                                 'nums':nums})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted=True
    return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted})

def all_events(request):
    event_list = Event.objects.all().order_by('event_date')
    return render(request, 'events/event_list.html', {'event_list':event_list})

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
