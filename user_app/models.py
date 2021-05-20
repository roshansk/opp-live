
from django.db import models
from django.http import request

from official_app.models import Station
from user_auth.models import User

# Create your models here.
class Complaint(models.Model):
    id = models.TextField(primary_key=True)
    applicant = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    complaint = models.TextField(null=False)
    response = models.TextField()
    station = models.ForeignKey(Station,on_delete=models.CASCADE)


    def get_complaint(self):
        return dict(
            id = self.id,
            applicant = self.applicant.get_user(),
            complaint = self.complaint,
            response = self.response,
            station = self.station.get_station(),
        )


class Request(models.Model):
    id = models.TextField(primary_key=True)
    applicant = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    request = models.TextField(null=False)
    response = models.TextField(null=True)
    station = models.ForeignKey(Station,on_delete=models.CASCADE)

    def get_request(self):
        return dict(
            id = self.id,
            applicant = self.applicant.get_user(),
            request = self.request,
            response = self.response,
            station = self.station.get_station(),
        )