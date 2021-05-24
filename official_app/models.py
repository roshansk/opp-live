from datetime import timezone
from django.db import models
from django.db.models.expressions import F
from django.db.models.fields import DateTimeField
from django.utils import timezone

import uuid
import os

from OPP.utils import get_states,get_all_districts

# Create your models here.

#choices
states = get_states()
districts = sorted(get_all_districts())
gender_choices = [ ('Male','Male'), ('Female','Female'), ('Transgender','Transgender'), ('other','Other') ]

#SET OFFENDER IMAGE PATH
def set_image_path_offender(instance,filename):
    basefilename,file_extension = os.path.splitext(filename)
    return "profile_picture/offender/{id}{ext}".format( id = instance.id, ext = file_extension)


class Station(models.Model):
    sid = models.TextField(primary_key=True,default=uuid.uuid4().hex[:8].upper())
    branch_name = models.TextField(unique=True,max_length=24)
    address = models.TextField(blank=False,null=False)
    state = models.TextField(choices=states,blank=False,null=False,default='')
    district = models.TextField(choices=districts,blank=False,null=False,default='')
    pincode = models.IntegerField(blank=False,null=False)

    def get_station(self):

        return dict(
            sid = self.sid,
            branch_name = self.branch_name,
            address = self.address,
            state = self.state,
            district = self.district,
            pincode = self.pincode
        )
        
class Notice(models.Model):
    nid = models.TextField(primary_key=True,default=uuid.uuid4().hex[:6].upper())
    issue_date = models.DateField(null=False,default=timezone.now)
    type = models.TextField(null=False)
    title = models.TextField(null=False)
    station = models.ForeignKey(Station,on_delete=models.CASCADE,default=None)
    description = models.TextField(null=False) 

class Offender(models.Model):
    id = models.TextField(primary_key=True,default=uuid.uuid4().hex[:6].upper())
    name = models.TextField(null=False)
    uid = models.TextField(unique=True,null=True,blank=True)
    gender = models.TextField(choices=gender_choices,default='OTHER')
    contact_number = models.CharField(null=False,unique=True,max_length=10,blank=True,default='')
    address = models.TextField(null=True)
    face_img = models.ImageField(upload_to=set_image_path_offender,default='user-regular.png')
    face_obj = models.TextField(unique=True,null=True)


    def get_offender(self) :
        
        return dict(
            id = self.id,
            name = self.name,
            gender = self.gender,
            contact_number = self.contact_number,
            address = self.address,
            face_img = self.face_img.url,
        )
    
class Offence(models.Model):
    id = models.TextField(primary_key=True,default=uuid.uuid4().hex[:6].upper())
    offence_reg_timestamp = DateTimeField(default=timezone.now)
    applicant_name = models.TextField(null=False)
    station =   models.ForeignKey(Station,null=False,on_delete=models.CASCADE,default=None)
    applicant_uid = models.TextField(null=True,blank=False)
    applicant_gender = models.TextField(choices=gender_choices,default='OTHER')
    applicant_contact_number = models.CharField(null=False,max_length=10)
    date_time_offence = models.DateTimeField(null=False,blank=False)
    offence_place = models.TextField(null=False,blank=False)
    offence_type = models.CharField(null=False,max_length=100,default='')
    offence_description = models.TextField(null=False,blank=False)
    offenders = models.ManyToManyField(Offender)
    n_offenders = models.IntegerField(null=True,default=0)
    status = models.TextField(choices=[('open','open'),('close','close')],default="open")

    def get_offence(self):
        
        return dict(
            id = self.id,
            registration_timestamp = self.offence_reg_timestamp,
            applicant_name = self.applicant_name,
            station = self.station.get_station(),
            applicant_uid = self.applicant_uid if self.applicant_uid else None,
            applicant_gender = self.applicant_gender,
            applicant_contact_number = self.applicant_contact_number,
            date_time_offence = self.date_time_offence,
            offence_place = self.offence_place,
            offence_type = self.offence_type,
            offence_description = self.offence_description,
            n_offenders = self.n_offenders,
            status  = self.status
        )







    
    

    