from django.urls import path
from . import views


urlpatterns = [
     
    path('',views.index,name='index'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('new_request/<str:sid>',views.new_request,name='new_request'),
    path('new_complaint/<str:sid>',views.new_complaint,name='new_complaint'),
    path('user_logout/',views.logout,name="user_logout"),
    path('profile/',views.profile,name="user_profile"),
    path('user_offenders/',views.user_offenders,name="user_offenders"),
    path('offence_details_user/<str:pk>',views.offence_details_user,name="offence_details_user"),
]