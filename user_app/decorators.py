from django.shortcuts import redirect
from django.contrib import messages


def login_required(view):
    def wrapper(request,*args,**kwargs):
        if 'user' in request.session :
            if request.session['user'] != None:
                return view(request,*args,**kwargs)
            else:
                messages.add_message(request,
                messages.WARNING,
                'You must be logged in to view this page.',
                extra_tags='alert  alert-warning alert-dismissible fade show my-3')
                return redirect('/user_auth/login')
        else :
            messages.add_message(request,
            messages.WARNING,
            'You must be logged in to view this page.',
            extra_tags='alert alert-warning alert-dismissible fade show my-3')
            return redirect('/user_auth/login')
    return wrapper