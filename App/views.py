# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, EVStation, EV, Slot
from django.http import HttpResponse, JsonResponse
import random
import json
from django.views.decorators.csrf import csrf_exempt
import math
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from datetime import datetime
from opencage.geocoder import OpenCageGeocode

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']

        # print("entered")

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
            return HttpResponse("User Already Exists")
        
        user = User(name=name, email=email, password=password, phone=phone)
        user.save()

        print("saved")

        messages.success(request, 'You have successfully registered')
        return redirect('home')

    return render(request, 'register.html')

def isSuperUser(email):
    return email == 'akhil@gmail.com'


def login(request):
    
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        print("post")

        # try:
        print(email, password)
        user = User.objects.get(email=email, password=password)
        
        print(user.email, user.password, email, password)
        request.session['user_details'] = {'email':email, 'password':password}
        print("session")

        if isSuperUser(email):
            # redirect('super_user_home')
            return render(request, 'super_user_home.html')
    

        return render(request, 'user.html', {'user': user})
        # except:
        #     print("INVALID")
        #     return HttpResponse("Invalid Email or Password")
    print("end")
    
    return render(request, 'home.html')

def user_page(request):
    return render(request, 'user.html')

def generate_random_location(box):
    latitude = random.uniform(box['min_lat'], box['max_lat'])
    longitude = random.uniform(box['min_lng'], box['max_lng'])
    return latitude, longitude

def create_ev_stations(request):
    # Define bounding box for Hyderabad
    # EVStation.objects.all().delete()
    HYDERABAD_BOX = {
        'min_lat': 22.6, 'max_lat': 22.8, 'min_lng': 75.7, 'max_lng': 75.9
    }

    # Generate 500 EV stations for Hyderabad
    city_stations_count = 0
    while city_stations_count < 500:
        latitude, longitude = generate_random_location(HYDERABAD_BOX)
        
        EVStation.objects.create(
            name=f"EV Station {city_stations_count + 1} - Hyderabad",
            latitude=latitude,
            longitude=longitude,
        )
        city_stations_count += 1
        print(f"EV Station {city_stations_count} - Latitude: {latitude}, Longitude: {longitude} (Hyderabad)")

    return redirect('home')
def generate_random_location(bounding_box):
    min_lat = bounding_box['min_lat']
    max_lat = bounding_box['max_lat']
    min_lng = bounding_box['min_lng']
    max_lng = bounding_box['max_lng']
    
    latitude = random.uniform(min_lat, max_lat)
    longitude = random.uniform(min_lng, max_lng)
    
    return latitude, longitude
    

def home(request):
    ev_stations = EVStation.objects.all()
    return render(request, 'home.html', {'ev_stations': ev_stations})


def get_ev_stations(request):
    ev_stations = EVStation.objects.all()
    ev_stations_json = json.dumps(list(ev_stations.values('name', 'latitude', 'longitude', )))
    print(ev_stations_json)
    return render(request, 'ev_stations_map_view.html', {'ev_stations_json': ev_stations_json})
    

@csrf_exempt
def save_user_location(request):
    if request.method == 'POST':
        print("entered")
        data = json.loads(request.body)
        latitude =  17.4933 # data.get('latitude')
        longitude = 78.3934 # data.get('longitude')
        print(latitude)
        
        if latitude is not None and longitude is not None:
            request.session['user_location'] = {'latitude': latitude, 'longitude': longitude}
            print("*****************************************")
            print(request.session['user_location'])
            print("*****************************************")
            return JsonResponse({'status': 'success'}, status=201)
        
        
        
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    

def find_evs(request):
    return render(request,'find_evs.html')


def get_evStations_by_km(request):

    km = request.POST.get('distance') 
    
    if(request.session['user_location'] is None):
        return HttpResponse("Please share your location")
    
    latitude = request.session['user_location']['latitude']
    longitude = request.session['user_location']['longitude']

    ev_stations = EVStation.objects.all()

    required_stations = []

    print(latitude, longitude)

    for station in ev_stations:
        
        if(distance(latitude,longitude,station.latitude,station.longitude)<=int(km)):
            st = {'name': station.name, 'latitude': station.latitude, 'longitude':station.longitude}

            required_stations.append(st)

    # print(latitude,longitude, km)

    # return HttpResponse("Success")

    ev_stations_json = json.dumps(required_stations)

    return render(request, 'ev_stations_map_view.html', {'ev_stations_json': ev_stations_json})



def distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Difference in latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance_km = R * c
    return distance_km


def get_user_location(request):
    
    user_location = request.session['user_location']

    if user_location:
        return JsonResponse({'latitude': user_location['latitude'], 'longitude': user_location['longitude']})
    else:
        return HttpResponse("Please share your location")
    

def get_coordinates(location_name):
    try:
        geocoder = OpenCageGeocode("37180c2d57694b32894e358b747ceff1")
        results = geocoder.geocode(location_name)
        if results and len(results):
            latitude = results[0]['geometry']['lat']
            longitude = results[0]['geometry']['lng']
            return latitude, longitude
        else:
            print("Location not found")
            return None, None
    except Exception as e:
        print(f"Geocoding failed: {e}")
        return None, None

def get_ev_stations_by_location(request):
    location = request.POST.get('location')

    latitude, longitude = get_coordinates(location)

    if latitude is None:
        print("None")
        return HttpResponse("Enter Correct Location Name")

    print(latitude, longitude)

    ev_stations = EVStation.objects.all()

    required_stations = []

    for station in ev_stations:
        
        if(distance(latitude,longitude,station.latitude,station.longitude)<10):
            st = {'name': station.name, 'latitude': station.latitude, 'longitude':station.longitude}

            required_stations.append(st)

    print(latitude,longitude)

    # return HttpResponse("Success")

    ev_stations_json = json.dumps(required_stations)

    print(ev_stations_json)

    return render(request, 'ev_stations_map_view.html', {'ev_stations_json': ev_stations_json})


    # return HttpResponse("Success")

def manage_account(request):
    context = request.session['user_details']
    email = context['email']

    context['name'] = User.objects.get(email = email).name
    
    context['phone'] = User.objects.get(email = email).phone

    print(context)

    return render(request,"manage_account.html", context = context)


def change_password(request):
    if(request.method=='POST'):
        present_password = request.POST.get('present_password')
        new_password = request.POST.get('new_password')

        email = request.session['user_details']['email']
        password = request.session['user_details']['password']

        print(email, password)

        if(present_password!=password):
            return HttpResponse("Incorrect Password")
        
        user = User.objects.get(email=email)

        print(user.password)

        user.password = new_password

        user.save()

        print(user)

        # print(User.objects.all())
        # users = User.objects.all()
        # for user in users:
        #     print(f"Name: {user.name}, Email: {user.email}, Password: {user.password}, Phone: {user.phone}")

        return HttpResponse("Password Changed Successfully")
        

    return render(request,'change_password.html')

def manage_your_ev_vehicles(request):
    return render(request, 'manage_your_ev_vehicles.html')

def add_ev(request):
    if(request.method=='POST'):
        email = request.session['user_details']['email']
        name = request.POST.get('name')
        number = request.POST.get('number')

        ev = EV(email = email, name = name, number = number)
        ev.save()

        return HttpResponse("EV details saved successfully")

    return render(request, 'add_ev.html')

def show_evs(request):
    # print("*************************************")
    email = request.session['user_details']['email']
    ev = EV.objects.filter(email = email)
    ev_json = json.dumps(list(ev.values('email','name', 'number')))
    ev_dict = json.loads(ev_json)
    if(len(ev_dict)==0):
        return HttpResponse("No EVs Found")
    # ev_dict[len(ev_dict)-1]['email'] = email
    print(ev_dict)

    return render(request, 'show_evs.html', context = {'evs': ev_dict})

def delete_ev(request, number):
    try:
        email = request.session['user_details']['email']
        ev = EV.objects.get(email = email, number = number)
        ev.delete()
        return HttpResponse("Successfully deleted")

    except:
        return HttpResponse("EV Number Not Found")



def book_nearby(request):
    user_location = request.session['user_location']

    latitude = user_location['latitude']
    longitude = user_location['longitude']

    ev_stations = EVStation.objects.all()

    print(user_location)

    required_stations = []

    for station in ev_stations:
        
        if(distance(latitude,longitude,station.latitude,station.longitude)<2):
            st = {'name': station.name, 'latitude': station.latitude, 'longitude':station.longitude}

            required_stations.append(st)
    
    ev_stations_json = json.dumps(required_stations)

    return render(request, 'ev_stations_map_view.html', {'ev_stations_json': ev_stations_json})

def book_by_place(request):
    # return render(request, 'ev_stations_map_view.html')
    location = request.POST.get('location')

    latitude, longitude = get_coordinates(location)

    print(location, latitude, longitude)

    if latitude is None:
        print("None")
        return HttpResponse("Enter Correct Location Name")

    print(latitude, longitude)

    ev_stations = EVStation.objects.all()

    required_stations = []

    for station in ev_stations:
        
        if(distance(latitude,longitude,station.latitude,station.longitude)<10):
            st = {'name': station.name, 'latitude': station.latitude, 'longitude':station.longitude}

            required_stations.append(st)

    # print(latitude,longitude, km)

    # return HttpResponse("Success")

    ev_stations_json = json.dumps(required_stations)

    return render(request, 'ev_stations_map_view.html', {'ev_stations_json': ev_stations_json})
    

def book_slot(request):
    # Handle the booking logic here
    
    return render(request, 'book_slot.html', {'station_name': 'station_name'})

def booking_page(request, station_name):
    if request.method == "POST":
        date = request.POST['date']
        time = request.POST['time']
        email = request.session['user_details']['email']

        request.session['station_name'] = station_name

        print(request.session.get('station_name'))

        Slot.objects.create(
            ev_station_name=station_name,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            time=datetime.strptime(time, '%H:%M').time(),
            email = email
        )
        
        return HttpResponse("Slot booked successfully.")
    else:
        request.session['station_name'] = station_name
        request.session.save()

        print(request.session.get('station_name'))
        return render(request, 'booking_page.html', {'station_name': station_name})


def view_bookings(request):
    # Slot.objects.all().delete()
    email = request.session['user_details']['email']
    slots = Slot.objects.filter(email=email)
    return render(request, 'view_bookings.html', {'slots': slots, 'email': email})

def remove_booking(request, booking_id):
    Slot.objects.get(booking_id = booking_id).delete()
    return HttpResponse("Deleted Successfully")

def payment_page(request):
    station_name = request.session['station_name']
    return render(request, 'payment_page.html', {'station_name' : station_name})

from django.urls import reverse

def payment_success(request):
    station_name = request.session.get('station_name')
    print(station_name)
    return redirect(f"{reverse('booking_page', kwargs={'station_name': station_name})}?payment_success=true")

def super_user_home(request):
    return render(request, 'super_user_home.html')

def show_all_users(request):
    users = User.objects.all()
    return render(request, 'show_all_users.html', {'users': users})

def add_ev_station(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        ev_station = EVStation.objects.create(name=name, latitude=latitude, longitude=longitude)
        ev_station.save()
        return HttpResponse("EV Station saved successfully")  # Redirect to a view that displays the list of EV stations
    else:
        return render(request, 'add_ev_station.html')