from django.urls import path
from .views import registerUser, loginUser

urlpatterns = [
    path('register/', registerUser , name='register'),
    path('login/', loginUser , name='login' ),
]