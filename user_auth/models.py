from django.db import models
from OPP.utils import get_states,get_all_districts
import os
# Create your models here.

def set_image_path_user(instance,filename):
    basefilename,file_extension = os.path.splitext(filename)
    return "profile_picture/citizen/{id}{ext}".format( id = instance.uid, ext = file_extension)

states = get_states()
all_districts = get_all_districts()

class User(models.Model):

    gender_choices = [ ('Male','Male'), ('Female','Female'), ('Transgender','Transgender'), ('Other','Other') ] 

    uid = models.TextField(primary_key=True)
    name = models.TextField(blank=False,null=False)
    gender = models.TextField(blank=False,null=False,choices=gender_choices ,default = 'Other' )
    username = models.TextField(unique=True,blank=False,null=False)
    profile_image = models.ImageField(upload_to=set_image_path_user,default='user-regular.png')
    img_obj = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    password = models.TextField(blank=False,null=False,default='')
    address = models.TextField(blank=True,null=True)
    state = models.TextField(choices=states,blank=True,null=True,default='')
    district = models.TextField(choices=all_districts,blank=True,null=True,default='')
    pincode = models.IntegerField(blank=True,null=True) 

    def get_user(self):
        return dict(

            uid = self.uid,
            name = self.name,
            gender = self.gender,
            username = self.username,
            profile_image = self.profile_image.url,
            address = self.address,
            state = self.state,
            district = self.district,
            pincode = self.pincode,

        )