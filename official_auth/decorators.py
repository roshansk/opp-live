from django.shortcuts import redirect
from django.http import HttpResponse

def official_logged_in(view):
    def wrapper(request,*args,**kwargs):
        if 'official' in request.session :
            if request.session['official'] != None:
                return redirect('/official_auth/login')
            else :
                return view(request,*args,**kwargs)    
        else :
            return view(request,*args,**kwargs)
    return wrapper