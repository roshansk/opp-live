from django.shortcuts import redirect, render
from  django.contrib import messages
import uuid

from user_app.models import Request,Complaint
from official_app.models import Offence, Station,Notice
from user_auth.models import User
from user_app.forms import RequestForm,ComplaintForm,ProfileUpdate
from user_app.decorators import login_required
# Create your views here.


def index(request):
    return render(request,'user_app/main.html',context={})

@login_required
def dashboard(request):

    user = request.session['user']
    user_obj = User.objects.get(uid=user['uid'])
    
    requests = Request.objects.filter(applicant=user_obj)
    complaints = Complaint.objects.filter(applicant=user_obj)
    stations = Station.objects.filter(district=user['district'])    
    offences = Offence.objects.filter(station__district=user['district'])
    notices = Notice.objects.filter(station__district=user['district'])

    print(notices)

    context = {
        'user':user,
        'requests':requests or [],
        'complaints':complaints or [],
        'offences':offences or [],
        'stations':stations or [],
        'notices':notices or []
    }

    return render(request,'user_app/dashboard.html',context)




@login_required
def new_request(request,sid):
    
    user = request.session['user']
    form = RequestForm(request.POST or None,initial={"id":"NONE"})
    station = Station.objects.get(sid=sid)
    

    if request.method == "POST" :
        if form.is_valid() : 
            req = form.save(commit=False)
            req.id = uuid.uuid4().hex[:8].upper()
            req.applicant = User.objects.get(uid=user['uid'])
            req.station = station
            req.save()
            return redirect('dashboard')


    context = {
        'station':station,
        'form' : form,
    }

    return render(request,'user_app/new_request.html',context)



@login_required
def new_complaint(request,sid):
    
    user = request.session['user']
    form = ComplaintForm(request.POST or None,initial={"id":"NONE"})
    station = Station.objects.get(sid=sid)

    if request.method == "POST" :
        if form.is_valid() : 
            complaint = form.save(commit=False)
            complaint.id = uuid.uuid4().hex[:8].upper()
            complaint.applicant = User.objects.get(uid=user['uid'])
            complaint.station = Station.objects.get(sid=sid)
            complaint.save()
            return redirect('dashboard')



    context = {
        'station':station,
        'form' : form,
    }

    return render(request,'user_app/new_complaint.html',context)


@login_required
def profile(request):

    user = request.session['user']
    user_obj = User.objects.get(uid=user['uid'])
    form = ProfileUpdate(instance=user_obj)
    

    if request.method == "POST" :
        form = ProfileUpdate( request.POST,request.FILES,instance=user_obj)
        if form.is_valid() :
            form.save()
            request.session['user'] = User.objects.get(uid=user['uid']).get_user()
            return redirect('dashboard')        

    context = {
    'user':user,
    'form':form,
    }

    return render(request,'user_app/profile.html',context)

@login_required
def logout(request):

    request.session.pop('user')

    return redirect('/user_auth/login')

@login_required
def user_offenders(request):

    context = {

    }
    return render(request,'user_app/offenders.html',context)


@login_required
def offence_details_user(request,pk):

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

        return render(request,'user_app/offence_details.html',context)

    else :
        messages.add_message(
                request,
                messages.INFO,
                'Case details you are looking for are out of session please check again under offences',
                extra_tags='alert alert-info alert-dismissible fade show my-2'

        )
        return redirect('dashboard')

    