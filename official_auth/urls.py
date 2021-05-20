from django.urls import path
from .views import login, registration

urlpatterns = [
    path('register/', registration , name='register'),
    path('login/', login , name='login' ),
]

