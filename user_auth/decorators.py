from django.shortcuts import redirect
from django.http import HttpResponse

def user_logged_in(view):
    def wrapper(request,*args,**kwargs):
        if 'user' in request.session :
            if request.session['user'] != None:
                return redirect('dashboard')
            else :
                return view(request,*args,**kwargs)    
        else :
            return view(request,*args,**kwargs)
    return wrapper