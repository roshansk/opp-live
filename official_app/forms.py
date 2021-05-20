#django imports
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db.models import fields
from django.forms import widgets
from .models import Notice, Offence, Offender, Station
from OPP.utils import get_all_districts, get_states

#python imports
import pickle

#self imports
from OPP.FaceREC import check_face
from OPP.utils import validate_mobile_number, validate_name, verify_adhaar
from user_app.models import Request,Complaint



class Station_Enrollment(forms.ModelForm):
    
    class Meta:
        
        model = Station
        
        fields = ['branch_name','state','address','district','pincode']
        
        states = get_states()
        
        widgets = {
            'branch_name':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(choices=states,attrs={'class':'form-control','id':'select-state'}),
            'address':forms.Textarea(attrs={'class':'form-control','rows':'3','placeholder':'Block Number/Building Number/Landmark'}),
            'district':forms.Select(choices=[],attrs={'class':'form-control','id':'select-district'}),
            'pincode':forms.TextInput(attrs={'type':'number','class':'form-control','placeholder':'6 digit Postal code'})
        }


class New_Notice(forms.ModelForm):

    class Meta:
        
        model = Notice
        
        fields = ['type','title','description','station']
        
        notice_types = [('Notice','Notice'),('Alert','Alert')]
        
        widgets = {
            'station':forms.Select(attrs={'class':'form-control','id':'sid','hidden':'true'}),
            'type':forms.Select(choices=notice_types,attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control','rows':'3','placeholder':'Detailed Description'}),
            
        }

class New_Offender(forms.ModelForm):
    
    class Meta:
        
        model = Offender
        
        fields = ['id','name','uid','gender','contact_number','address','face_img']
        
        widgets = {
            'id':forms.TextInput(attrs={'type':'text','hidden':'true'}),
            'name':forms.TextInput( attrs={ 'type':'text', 'class': 'form-control offender-input', 'placeholder':'Firstname   Middlename   Lastname' } ),
            'uid':forms.TextInput( attrs={ 'type':'number', 'class': 'form-control offender-input' , 'placeholder':'12 digit UID eg 123456789012' } ),
            'gender':forms.Select(attrs={ 'class': 'form-control offender-input'}),
            'contact_number':forms.TextInput(attrs={'type':'number','class':'form-control offender-input','placeholder':'10 digit phone number'}),
            'address':forms.Textarea( attrs={'class':'form-control','rows':'3','Placeholder':'Block/Flat No., Building, Street, City, POSTAL code(Pincode).'} )           
        }


    def clean(self):

        errors = {}
        cleaned_data = super(New_Offender, self).clean()
        
        uid = cleaned_data.get('uid')
        name = cleaned_data.get('name')
        contact_number = cleaned_data.get('contact_number')         
        face_img = cleaned_data.get('face_img')
        res = check_face(face_img)

        if uid :
            if verify_adhaar(uid) == False:
                errors['uid'] = ("Adhaar number is not valid.")
        if validate_name(name) == False:
            errors['name'] = ("Name must be in order 'Firstname  Middlename  Lastname'")
        if contact_number :
            if validate_mobile_number(contact_number) == None :
                errors['contact_number'] = ("Contact Number must be 10 digit and start from 7, 8 or 9.")
        if res['detected'] == False :
            errors['face_img'] = (res['error'])
        if errors :
            raise ValidationError(errors)

        cleaned_data['face_obj'] = pickle.dumps(res['encoding'])

        return cleaned_data


class New_Offence(forms.ModelForm):
    
    class Meta:
        
        model = Offence
        
        fields = ['id','applicant_name','applicant_uid','applicant_gender','applicant_contact_number','date_time_offence','offence_type','offence_place','offence_description']
        
        widgets = {
            'id':forms.TextInput(attrs={'type':'text','hidden':'true'}),
            'applicant_name':forms.TextInput( attrs={ 'type':'text', 'class': 'form-control ', 'placeholder':'Firstname   Middlename   Lastname' } ),
            'applicant_uid':forms.TextInput( attrs={ 'type':'number', 'class': 'form-control ' , 'placeholder':'12 digit UID eg 123456789012' } ),
            'applicant_gender':forms.Select( attrs={ 'class': 'form-control '} ),
            'applicant_contact_number':forms.TextInput( attrs={'type':'number','class':'form-control','placeholder':'10 digit phone number'} ),
            'date_time_offence':forms.DateTimeInput( attrs={'type':'datetime-local','class':'form-control'} ),
            'offence_place':forms.Textarea( attrs={'class':'form-control ','rows':'3','Placeholder':'Detailed Address'} ),
            'offence_type':forms.TextInput(attrs={'class':'form-control','placeholder':'Type/Name of Offence Under Section Number __ '}),
            'offence_description':forms.Textarea( attrs={'class':'form-control ','rows':'3','Placeholder':'Detailed Description'} ),
        }

    def clean(self):

        errors = {}
        cleaned_data = super(New_Offence, self).clean()
        uid = cleaned_data.get('applicant_uid')
        name = cleaned_data.get('applicant_name')
        contact_number = cleaned_data.get('applicant_contact_number')

        if verify_adhaar(uid) == False:
            errors['applicant_uid'] = ("Adhaar number is not valid.")
        if validate_name(name) == False:
            errors['applicant_name'] = ("Name must be in order 'Firstname  Middlename  Lastname'")
        if validate_mobile_number(contact_number) == None :
            errors['contact_number'] = ("Contact Number must be 10 digit and start from 7, 8 or 9.")
        if errors :
            raise ValidationError(errors)




class Station_Details(forms.Form):

    states = get_states()

    state = forms.ChoiceField(
        choices = states,
        widget = forms.Select( attrs={ 'class':'form-select form-select-sm','id':'select-state',} )
    )

    district = forms.ChoiceField(
        choices = get_all_districts(), 
        widget = forms.Select( attrs={ 'class':'form-select form-select-sm','id':'select-district'} )
    )

    pincode = forms.CharField(
        required=False,
        max_length=6,
        widget = forms.TextInput( attrs = {'class':'form-control','type':'number','id':'pincode'} ) 
    )

    
    def clean(self):

        errors = {}

        state = self.cleaned_data['state']
        district = self.cleaned_data['district']
        pincode = self.cleaned_data['pincode'] 

        
        if pincode : 
            if len(pincode) != 6 :
                errors['pincode'] = 'PINCODE must be 6 numbers long'
        if errors :
            raise ValidationError(errors)



class Request_Response_Form(forms.ModelForm):
    
    class Meta :
        model = Request
        fields = ["response"]
        widgets = {
            "response":forms.Textarea( attrs={ 'class':'form-control', 'rows':'5' , 'placeholder':'Response','required':'true'} )
        }


class Complaint_Response_Form(forms.ModelForm):
    
    class Meta :
        model = Complaint
        fields = ["response"]
        widgets = {
            "response":forms.Textarea( attrs={ 'class':'form-control', 'rows':'5' , 'placeholder':'Response','required':'true'})
        }
    