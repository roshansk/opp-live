
from os import name
from django.urls import path
from . import views

urlpatterns = [
    
    path('main/',views.main,name='main'),

    path('station_enrollment/',views.station_enrollment , name='station_enrollment'),
    path('delete_station/<str:sid>',views.delete_station,name='delete_station'),
    
    path('get_districts/<str:state>',views.post_districts,name='get_districts'),
    
    path('new_notice/',views.new_notice,name='new_notice'),
    path('delete_notice/<str:nid>',views.delete_notice,name='delete_notice'),

    path('new_offence/',views.new_offence,name='new_offence'),
    path('add_offender/<str:pk>',views.add_offender,name='add_offender'),
    path('add_known_offender/<str:oid>/<str:cid>',views.add_known_offender,name='add_known_offender'),
    path('remove_offender/<str:oid>/<str:cid>',views.remove_offender,name='remove_offender'),
    path('offence_details/<str:pk>',views.offence_details,name='offence_details'),
    path('change_offence_status/<str:pk>',views.change_offence_status,name='change_offence_status'),

    path('search_offenders',views.search_offenders,name='search_offenders'),


    path('logout/',views.logout,name='logout'),

    path('profile/',views.profile,name='profile'),

    path('station/',views.update_station_details,name='station'),

    path('enlist_station/<str:id>',views.enlist_station_confirmation,name='enlist_station'),

    path('complaint_response/<str:id>',views.complaint_response,name='complaint_response'),
    path('request_response/<str:id>',views.request_response,name='request_response'),

]