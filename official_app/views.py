#imports
#django
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import messages

from django.http.response import HttpResponse
from django.shortcuts import redirect, render

#python
import json
import uuid

#self/app
from user_app.models import Request,Complaint
from official_app.decorators import login_required
from official_auth.models import Official
from .forms import New_Offence, New_Offender, Station_Details, Station_Enrollment, New_Notice,Request_Response_Form,Complaint_Response_Form
from official_auth.forms import Profile_Update

from OPP.utils import get_districts,get_districts_dict
from .models import Notice, Offence, Offender, Station

# Create your views here.



#Official Main Page
@login_required
def main(request):
    
    official = request.session.get('official')
    requests = []
    station = None
    offences = []
    notices = []
    complaints = []

    if official['station'] :
        station = Station.objects.get(sid=official['station']['sid'])
        requests = Request.objects.filter(station=station) or None
        offences = Offence.objects.filter(station=station ) or None
        notices = Notice.objects.filter(station=station) or None
        complaints = Complaint.objects.filter(station=station) or None

    context = {
        'requests':requests or [],
        'official':official,
        'station':station or [],
        'offences':offences or [],
        'notices':notices or [],
        'complaints':complaints or []
    }
    
    return render(request,'official_app/main.html',context)



#Station Registration Page
@login_required
def station_enrollment(request):

    form = Station_Enrollment() 

    if request.method == 'POST' :
        form = Station_Enrollment(data=request.POST)
        if form.is_valid() :
            form.save()
            messages.add_message(
                request,
                messages.INFO,
                'Station {branch} has been registered under {district},{state}'.format(branch=form.cleaned_data['branch_name'],district=form.cleaned_data['district'],state=form.cleaned_data['state'])
            )
            return redirect('/official_app/station')

    context = {
        'form':form
    }
    
    return render(request,'official_app/station_enrollment.html',context)


#Delete Station
@login_required
def delete_station(request,sid):
    station = Station.objects.filter(sid = sid).delete()
    return HttpResponse('Object deleted')



#GET Districts for Station Registration
def post_districts(request,state):
    data = {}
    if request.method == 'GET':
        districts = get_districts(state)
        data = json.dumps(districts)
    return HttpResponse(data,content_type="application/json")


#New Notice
@login_required
def new_notice(request):

    official = request.session['official']
    station = official['station']
    station_obj = Station.objects.get(sid = station['sid'])

    form = New_Notice()
    form.fields['station'].initial = station_obj

    if request.method == 'POST':                
        form = New_Notice(data=request.POST)
        if form.is_valid() :
            form.save()
            return redirect('main')

    context = {
        'form':form,
    }
    return render(request,'official_app/new_notice.html',context)


#Delete Notice
@login_required
def delete_notice(request,nid):

    notice = Notice.objects.filter(nid=nid)
    
    if notice : 
        notice.delete()
        return redirect('main')
    else :
        res = "<h2>Notice Does Not exists</h2>"
    return redirect('main')


#NEW OFFENCE
@login_required
def new_offence(request):
    
    offence_form = New_Offence()
    offender_form = New_Offender()

    official = request.session['official']
    station = official['station']
    station_obj = Station.objects.get( sid = station['sid'] )

    if request.method == 'POST' :

        offence_form = New_Offence(data=request.POST)
        
        if offence_form.is_valid() :

            temp_offence = offence_form.save(commit=False)
            temp_offence.station = station_obj
            id_exists = Offence.objects.filter(id=offence_form.data.get('id'))
            
            if id_exists != None :
                temp_offence.id = uuid.uuid4().hex[:6].upper()           

            temp_offence.save()
            
            offence_data = temp_offence.get_offence()
            offence_data['registration_timestamp'] = json.dumps(offence_data['registration_timestamp'],cls=DjangoJSONEncoder)
            offence_data['date_time_offence'] = json.dumps(offence_data['date_time_offence'],cls = DjangoJSONEncoder)
            request.session['offence_details'] = offence_data
            return redirect('offence_details',pk=offence_data['id'])

    
    context = {
        'offence':offence_form,
        'offender':offender_form
    }

    return render(request,'official_app/new_offence.html',context)


#profile page
@login_required
def profile(request):

    official = request.session['official']
    official_instance = Official.objects.get(pid = official['id'])

    profile_form = Profile_Update(instance = official_instance)
    
    if official['state'] :
        districts = get_districts_dict(official['state'])
        profile_form.fields['district'].choices = districts
        profile_form.fields['district'].initial = official['district']


    
    if request.method == 'POST' :
        profile_form = Profile_Update(request.POST,request.FILES,instance=official_instance)
        if profile_form.is_valid():
            profile_form.save()
            request.session['official'] = official_instance.get_official()
            return redirect('/official_app/profile')

    context = {
        'official':official,
        'profile':profile_form,
    }

    return render(request,'official_app/profile_update.html',context)


#UPDATE STATION DETAILS
@login_required
def update_station_details(request):

    official = request.session['official']
    stations = []
    enrolled_station = []
    form = Station_Details() 
    
    if request.method == 'GET' and official['state'] and official['district'] :
        form.fields['state'].initial = official['state']
        form.fields['district'].choices = get_districts_dict(official['state'])
        form.fields['district'].initial = official['district']
        stations = Station.objects.filter( district = official['district'] )
        if not stations :
            messages.add_message(
                request,
                messages.INFO,
                'No Stations under district {district}'.format(district = official['district']),
                extra_tags='alert alert-info alert-dismissible fade show'
            )
    
    if request.method == 'POST' :

        form = Station_Details(request.POST)
        print(request.session['official'])
        if form.is_valid() :
            state = form.data['state']
            district = form.data['district']
            pincode = form.data['pincode']        

            if pincode :
                stations = Station.objects.filter( pincode = pincode )
                if not stations :
                    messages.add_message(
                    request,
                    messages.INFO,
                    'No Stations in Area with POSTAL CODE {pincode}'.format(pincode = pincode),
                    extra_tags='alert alert-info alert-dismissible fade show'
                    )
            else :
                stations = Station.objects.filter( district = district)
                if not stations :
                    messages.add_message(
                    request,
                    messages.INFO,
                    'No Stations under district {district}'.format(district = district),
                    extra_tags='alert alert-info alert-dismissible fade show'
                    )


    context = {
        'official':official,
        'stations':stations,
        'form':form
    }

    return render(request,'official_app/station_details.html',context)

#ENLIST STATION-CONFIRMATION
@login_required
def enlist_station_confirmation(request,id):

    official = request.session['official']
    station_obj = Station.objects.get(sid=id)
    station = station_obj.get_station()
    officials = []
    official_objs = Official.objects.filter(sid=station_obj)

    if not official_objs :
        officials = []
    else :
        for official_obj in official_objs :
            temp = official_obj.get_official()
            officials.append(temp)
    if request.method == 'POST' :
        data = request.POST
        if 'check-confirm' in data :

            official_obj = Official.objects.get(pid=official['id'])
            official_obj.sid = station_obj
            official_obj.save()
            request.session['official'] = official_obj.get_official()

            return redirect('/official_app/station')
        else :
            messages.add_message(
                    request,
                    messages.INFO,
                    'Please check above checkbox to continue.',
                    extra_tags='alert alert-warning alert-dismissible fade show my-2'
            )

    context={
        'station':station,
        'officials':officials
    }
    return render(request,'official_app/station_confirmation.html',context)    

#OFFICIAL_LOGOUT
@login_required
def logout(request):
    request.session['official'] = None
    return redirect('/official_auth/login')

#VIEW OFFENCE DETAILS
@login_required
def offence_details(request,pk):

    offenders = []

    offence_obj = Offence.objects.get(id=pk)
    
    if offence_obj :
        offence_details = offence_obj.get_offence()
        
        if offence_details['n_offenders'] > 0 :
           obj = Offence.objects.get(id = offence_details['id'])
           for offender in obj.offenders.all() :
               offenders.append(offender.get_offender())

        context = {
            'offence_details':offence_details,
            'offenders':offenders 
        }

        return render(request,'official_app/offence_details.html',context)

    else :
        messages.add_message(
                request,
                messages.INFO,
                'Case details you are looking for are out of session please check again under offences',
                extra_tags='alert alert-info alert-dismissible fade show my-2'

        )
        return redirect('/official_app/main')


#ADD OFFENDERS

def add_offender(request,pk):

    form = New_Offender()
    offence_obj = Offence.objects.get(id=pk)
    
    if offence_obj :
        offence_details = offence_obj.get_offence()

        if request.method == "POST" :

            form = New_Offender(request.POST,request.FILES)

            if form.is_valid() :
                temp = form.save()    
                temp.face_obj = form.cleaned_data['face_obj']
                temp.save()
                offence_obj.offenders.add(temp)
                offence_obj.n_offenders += 1
                offence_obj.save()
                offence_details = offence_obj.get_offence()
                return redirect('offence_details',pk=offence_details['id'])
            else :
                print(form.errors)

        context = {
            'offence_details':offence_details,
            'form':form
        }

        return render(request,'official_app/add_offender.html',context)

    else :
        messages.add_message(
                request,
                messages.INFO,
                'Case details you are looking for are out of session please check again under offences',
                extra_tags='alert alert-info alert-dismissible fade show my-2'

        )
        return redirect('/official_app/main')


#ADD OFFENDER FROM SEARCH BY
def add_known_offender(request,oid,cid):

    offence_obj = Offence.objects.get(id=cid)

    if offence_obj.offenders.all() :
        registered_offenders = offence_obj.offenders.all()
        for offender in registered_offenders :
            if offender.id == oid :
                messages.add_message(
                    request,
                    messages.INFO,
                    'Offender you attempted to register to this offence is already registered check under offender list.',
                    extra_tags='alert alert-info alert-dismissible fade show mb-2'

                )
                return redirect('offence_details',pk=offence_obj.id)

    offender = Offender.objects.get(id=oid)
    offence_obj.offenders.add(offender)
    offence_obj.n_offenders += 1
    offence_obj.save()
    messages.add_message(
        request,
        messages.INFO,
        'Offender is registered successfully check under offender list.',
        extra_tags='alert alert-info alert-dismissible fade show mb-2'

    )
    return redirect('offence_details',pk=offence_obj.id)


def remove_offender(request,oid,cid):
    
    offence_obj = Offence.objects.get(id=cid)
    offender_obj = Offender.objects.get(id=oid)

    if offence_obj.offenders.all() :
        offenders = offence_obj.offenders.all() 
        if offender_obj in offenders :
            offence_obj.n_offenders -= 1
            offence_obj.save()
            offence_obj.offenders.remove(offender_obj)

            messages.add_message(
                request,
                messages.INFO,
                'Offender - {name} is been removed from this offence.'.format(name=offender_obj.name),
                extra_tags='alert alert-info alert-dismissible fade show my-2'
            )


    return redirect('offence_details',pk=cid)


def change_offence_status(request,pk):

    offence_obj = Offence.objects.get(id=pk)

    if offence_obj.status == "open" :
        offence_obj.status = "closed"
        offence_obj.save()
        messages.add_message(
            request,
            messages.INFO,
            'Investigation for this offence is successfully closed.',
            extra_tags='alert alert-info alert-dismissible fade show my-2'
        )

    else :
        offence_obj.status = "open"
        offence_obj.save()
        messages.add_message(
            request,
            messages.INFO,
            'Investigation for this offence is successfully reopened.',
            extra_tags='alert alert-info alert-dismissible fade show my-2'
        )


    return redirect('offence_details',pk=offence_obj.id)


def search_offenders(request):

    context = {

    }
    return render(request,'official_app/search_offenders.html',context)



def complaint_response(request,id):

    form = Complaint_Response_Form()
    complaint = Complaint.objects.get(id=id)
    user = complaint.applicant
    
    if request.method == "POST":
        form = Request_Response_Form(request.POST,instance=complaint)
        if form.is_valid() :
            form.save()
            return redirect('main')


    context = {
        "form":form,
        "complaint":complaint,
        "user":user,
    }

    return render(request,'official_app/complaint_response.html',context)

def request_response(request,id):

    form = Request_Response_Form()
    request_obj = Request.objects.get(id=id)
    user = request_obj.applicant
        
    if request.method == "POST":
        form = Request_Response_Form(request.POST,instance=request_obj)
        if form.is_valid() :
            form.save()
            return redirect('main')

    context = {
        "form":form,
        "request":request_obj,
        "user":user,
    }

    return render(request,'official_app/request_response.html',context)