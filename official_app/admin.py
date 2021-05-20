from django.contrib import admin
from .models import Offence, Offender,Notice

# Register your models here.

admin.site.register(Notice)
admin.site.register(Offender)
admin.site.register(Offence)