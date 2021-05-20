#DAJNGO IMPORTS

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm,TextInput
from .models import Official


#PYTHON IMPORTS

import re

#SELF IMPORTS

from OPP.utils import  get_states, validate_password, verify_adhaar, validate_name


class Reg_form(ModelForm):
    cpass = forms.CharField(widget=TextInput( attrs={ 'type':'password', 'class': 'form-control','placeholder':'Match password' } ))

    class Meta:
        model = Official
        fields = ['oid','pid','name','desgn','password']
        widgets = {
            'oid':TextInput( attrs={ 'type':'number', 'class': 'form-control' , 'placeholder':'12 digit UID eg 123456789012' } ),
            'pid':TextInput( attrs={ 'type':'text', 'class': 'form-control', 'placeholder':'eg. KP124323G'  } ),
            'desgn':forms.Select( attrs={ 'class':'form-control' } ),
            'name':TextInput( attrs={ 'type':'text', 'class': 'form-control', 'placeholder':'Firstname   Middlename   Lastname' } ),
            'password':TextInput( attrs={ 'type':'password', 'class': 'form-control', 'placeholder':'Minimum 6 characters long must contain a special character(@#$%^&&+=).' } ),
        }
    
    def clean(self):

        errors = {}
        cleaned_data = super(Reg_form, self).clean()
        uid = cleaned_data.get('oid')
        name = cleaned_data.get('name')
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("cpass")

        if password != confirm_password:
            errors['cpass'] = ("Passwords do not match!")
        if verify_adhaar(uid) == False:
            errors['oid'] = ("Adhaar number is not valid.")
        if validate_name(name) == False:
            errors['name'] = ("Name must be in order 'Firstname  Middlename  Lastname '")
        if validate_password(password) == False and validate_password(confirm_password) == False:
            errors['password'] = ("Password must be 6 characters or longer and contain a special character(@#$%^&&+=).")
        if errors :
            raise ValidationError(errors)
        


class Login_form(forms.Form):
    pid = forms.CharField(widget=TextInput( attrs={ 'type':'text', 'class': 'form-control', 'placeholder':'eg. KP124323G'  } ))
    password = forms.CharField(widget=TextInput( attrs={ 'type':'password', 'class': 'form-control','placeholder':'#####' } ))



class Profile_Update(forms.ModelForm):


    class Meta: 
        model = Official
        fields = ['pid','oid','name','gender','profile_image','desgn','address','state','district','pincode']

        widgets = {
            'pid':forms.TextInput( attrs={ 'disabled':'true', 'class':'form-control' } ),
            'oid':forms.TextInput( attrs={ 'disabled':'true', 'class':'form-control' } ),
            'name':forms.TextInput( attrs={ 'disabled':'true', 'class':'form-control' } ),
            'gender':forms.Select( attrs={ 'class':'form-control' } ),
            'desgn':forms.Select(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control','id':'select-state'}),
            'profile_image':forms.FileInput(),
            'address':forms.Textarea(attrs={'class':'form-control','rows':'3','placeholder':'Block Number/Building Number/Landmark'}),
            'district':forms.Select(choices=[],attrs={'class':'form-control','id':'select-district'}),
            'pincode':forms.TextInput(attrs={'type':'number','class':'form-control','placeholder':'6 digit Postal code'})
        }
