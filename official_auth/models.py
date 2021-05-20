
from OPP.utils import get_all_districts, get_states
from django.db import models
from official_app.models import Station

# Create your models here.

import os


class Official(models.Model):

    def set_image_path(instance,filename):
        basefilename,file_extension = os.path.splitext(filename)
        return "profile_picture/official/{id}{ext}".format( id = instance.pid, ext = file_extension)


    ranks = [('Director General of Police (DGP)','Director General of Police (DGP)'),
            ('Additional Director General Of Police (ADGP)',' Additional Director General Of Police (ADGP)'),
            ('Inspector General Of Police/ Special Inspector General Of Police (IGP/SIGP)','Inspector General Of Police/ Special Inspector General Of Police (IGP/SIGP)'),
            ('Deputy Inspector General Of Police (DIGP)','Deputy Inspector General Of Police (DIGP)'),
            ('Superintendent of Police/Deputy Commissioner Of Police (SP/DCP)','Superintendent of Police/Deputy Commissioner Of Police (SP/DCP)'),
            ('Superintendent of Police/Deputy Commissioner Of Police (Junior Management Level)','Superintendent of Police/Deputy Commissioner Of Police (Junior Management Level)'),
            ('Additional Superintendent Of Police/Deputy Commissioner of Police (ASP/DCP)','Additional Superintendent Of Police/Deputy Commissioner of Police (ASP/DCP)'),
            ('Police Inspector (P.I.)','Police Inspector (P.I.)'),
            (' Assistant Police Inspector (A.P.I.)',' Assistant Police Inspector (A.P.I.)'),
            ('Police Sub-Inspector (SI)','Police Sub-Inspector (SI)'),
            ('Assistant Police Sub-Inspector (ASI)','Assistant Police Sub-Inspector (ASI)'),
            ('Head Constable (HC)','Head Constable (HC)'),
            ('Police Constable (PC)','Police Constable (PC)') 
    ]

    gender_choices = [ ('MALE','Male'), ('FEMALE','Female'), ('TRANSGENDER','Transgender'), ('OTHER','Other') ]

    states = get_states()
    all_districts = get_all_districts()

    oid = models.TextField(primary_key=True)
    pid = models.TextField(unique=True)
    sid = models.ForeignKey(Station,blank=True,null=True,on_delete=models.CASCADE)
    name = models.TextField(blank=False,null=False)        
    gender = models.TextField(blank=False,null=False,choices=gender_choices ,default = 'OTHER' )
    profile_image = models.ImageField(upload_to=set_image_path,default='user-regular.png')
    img_obj = models.TextField(blank=True)
    desgn = models.TextField(choices=ranks,blank=False)
    password = models.TextField(blank=False,null=False,default='')
    address = models.TextField(blank=True,null=True)
    state = models.TextField(choices=states,blank=True,null=True,default='')
    district = models.TextField(choices=all_districts,blank=True,null=True,default='')
    pincode = models.IntegerField(blank=True,null=True)


    def get_official(self) :
        
        return dict(
   

            name = self.name,
            id = self.pid,
            uid = self.oid,
            station = self.sid.get_station() if self.sid else None,
            profile_img = self.profile_image.url,
            desgn = self.desgn,
            address = self.address,
            state = self.state,
            district = self.district,
            pincode = self.pincode,
            
        )
    
    