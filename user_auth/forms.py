#DAJNGO IMPORTS
from django.forms import ModelForm, TextInput ,CharField, Form
from django.core.exceptions import ValidationError

#PYTHON IMPORTS
import re

#SELF IMPORTS
from .models import User
from OPP.utils import validate_name, validate_password, validate_username, verify_adhaar
from official_auth.models import Official

class register_user(ModelForm):

    cpass = CharField(widget=TextInput( attrs={ 'type':'password', 'class': 'form-control','placeholder':'Match password' } ))
    
    class Meta:
        model = User
        fields = ['uid','name','username','password']

        widgets = {
            'uid':TextInput( attrs={ 'type':'number', 'class': 'form-control' , 'placeholder':'12 digit UID eg 123456789012' } ),
            'name':TextInput( attrs={ 'type':'text', 'class': 'form-control', 'placeholder':'Firstname   Middlename   Lastname' } ),
            'username':TextInput( attrs={ 'type':'text', 'class': 'form-control', 'placeholder':'Eg. jhondoe321, special characters allowed(@#&*.) '} ),
            'password':TextInput( attrs={ 'type':'password', 'class': 'form-control', 'placeholder':'Minimum 6 characters long must contain a special character(@#$%^&&+=).' } ),
        }

    def clean(self) :
        errors = {}
        data = super(register_user,self).clean()

        uid = data.get('uid')
        username = data.get('username')
        name = data.get('name')
        password = data.get("password")
        confirm_password = data.get("cpass")

        try:
            user = Official.objects.get(oid = uid)
            if user == None :
                user = User.objects.get(oid = uid)
        except Official.DoesNotExist :
            user = None


        if password != confirm_password:
            errors['cpass'] = ("Passwords do not match!")
        if verify_adhaar(uid) == False:
            errors['uid'] = ("Adhaar number is not valid.")
        if user != None :
            errors['uid'] = ("User with this Adhaar Number already exists")
        if validate_name(name) == False:
            errors['name'] = ("Name must be in order 'Firstname  Middlename  Lastname")
        if validate_username(username) == False:
            errors['username'] = ("Username must be 4-12 characters long")
        if validate_password(password) == False and validate_password(confirm_password) == False:
            errors['password'] = ("Password must be 6 characters or longer and contain a special character(@#$%^&&+=).")
        if errors :
            raise ValidationError(errors)


class login_user(Form):
    username = CharField(widget=TextInput( attrs={ 'type':'text', 'class': 'form-control', 'placeholder':'eg. jhonDoe123'  } ))
    password = CharField(widget=TextInput( attrs={ 'type':'password', 'class': 'form-control','placeholder':'#####' } ))
