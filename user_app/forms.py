from django.db.models import fields
from user_auth.models import User
from django import forms
from user_app.models import Complaint, Request,Request

class ComplaintForm(forms.ModelForm):

    class Meta :
        model = Complaint
        fields = ["id","complaint"]
        widgets = {
            "id":forms.HiddenInput(),
            "complaint":forms.Textarea( attrs={'rows':'6','Placeholder':'Nature/Type and Description','class':'form-control'}), 
        }
    

class RequestForm(forms.ModelForm):

    class Meta :
        model = Request
        fields = ["id","request"]
        widgets = {
            "id":forms.HiddenInput(),
            "request":forms.Textarea( attrs={'rows':'6','Placeholder':'Nature/Type and Description','class':'form-control'}),
        }

class ProfileUpdate(forms.ModelForm):

    class Meta:
        model = User
        fields = ["name","gender","username","address","profile_image","pincode","state","district"]
        widgets = {
            'name':forms.TextInput( attrs={'class':'form-control' } ),
            'username':forms.TextInput( attrs={'class':'form-control' } ),
            'gender':forms.Select( attrs={ 'class':'form-control' } ),
            'state':forms.Select(attrs={'class':'form-control','id':'select-state'}),
            'profile_image':forms.FileInput(attrs={'class':'form-control','accept':'image/jpg, image/jpeg, .jpeg, .jpg'}),
            'address':forms.Textarea(attrs={'class':'form-control','rows':'3','placeholder':'Block Number/Building Number/Landmark'}),
            'district':forms.Select(choices=[],attrs={'class':'form-control','id':'select-district'}),
            'pincode':forms.TextInput(attrs={'type':'number','class':'form-control','placeholder':'6 digit Postal code'})
        }

