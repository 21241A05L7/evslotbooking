from django.urls import path
from .views import register, home, user_page, login, create_ev_stations, get_ev_stations, save_user_location, get_evStations_by_km, find_evs, get_ev_stations_by_location, manage_account, change_password, manage_your_ev_vehicles, add_ev, show_evs, delete_ev, book_nearby, book_by_place, book_slot, booking_page, view_bookings, remove_booking, payment_success, payment_page, get_ev_stations, add_ev_station, show_all_users

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('user/', user_page, name='user'),
    path('login/', login, name='login'),
    path('create_ev_stations/', create_ev_stations, name='create_ev_stations'),
    path('get_ev_stations/', get_ev_stations, name='get_ev_stations'),
    path('save_user_location/', save_user_location, name='save_user_location'),
    path('get_evStations_by_km/', get_evStations_by_km, name = 'get_evStations_by_km'),
    path('find_evs/', find_evs, name = 'find_evs'),
    path('get_ev_stations_by_location/', get_ev_stations_by_location, name = 'get_ev_stations_by_location'),
    path('manage_account/', manage_account, name = 'manage_account'),
    path('change_password/', change_password, name='change_password'),
    path('manage_account/', manage_account, name = 'manage_account'),
    path('manage_your_ev_vehicles', manage_your_ev_vehicles, name = 'manage_your_ev_vehicles'),
    path('add_ev/', add_ev, name = 'add_ev'),
    path('show_evs/', show_evs, name = 'show_evs'),
    path('delete_ev/<str:number>/', delete_ev, name = 'delete_ev'),
    path('book_nearby/', book_nearby, name = 'book_nearby'),
    path('book_by_place/', book_by_place, name = 'book_by_place'),
    path('book_slot/', book_slot, name='book_slot'),
    path('booking_page/<str:station_name>/', booking_page, name = 'booking_page'),
    path('view_bookings/', view_bookings, name = 'view_bookings'),
    path('remove_booking/<uuid:booking_id>', remove_booking, name = 'remove_booking'),
    path('payment_success/', payment_success, name = 'payment_success'),
    path('payment_page', payment_page, name = 'payment_page'),
    path('show_all_users', show_all_users, name="show_all_users"),
    path('show_all_ev_stations', get_ev_stations, name = 'show_all_ev_stations'),
    path('add_ev_station', add_ev_station, name = 'add_ev_station'),

]
