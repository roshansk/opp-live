

from django.shortcuts import redirect, render
from django.contrib.auth import hashers
from django.contrib import messages


from .forms import Login_form, Reg_form
from .models import Official
from official_auth.decorators import official_logged_in


# Create your views here.
@official_logged_in #check if official is logged in already
def registration(request):
    if request.method == 'POST':
        form = Reg_form(data=request.POST)
        if form.is_valid() :
            confirm = form.save(commit=False)
            confirm.name = str.capitalize(confirm.name)
            confirm.password = hashers.make_password(form.cleaned_data['password'],salt=form.cleaned_data['oid'],hasher='default')
            confirm.save()
            official = Official.objects.get(pid=form.cleaned_data['pid'])
            request.session['official'] = official.get_official()
            messages.add_message(
                        request,
                        messages.INFO,
                        'Welcome {name}, you have successfully registered please update profile and station details to access services'.format(name=confirm.name),
                        extra_tags='alert alert-warning alert-dismissible fade show my-3'
                    )
            return redirect('/official_app/main')
        else:
            print(form.errors)
    else:
        form = Reg_form()

    return render( request , 'official_auth/register.html' , { 'form':form } )

@official_logged_in
def login(request):
    if request.method == 'POST':
        form = Login_form(data=request.POST)
        if form.is_valid() :
            try:
                user = Official.objects.get(pid=request.POST['pid'])
            except Official.DoesNotExist :
                user = None
            if user :
                password = hashers.make_password(form.cleaned_data['password'],salt=user.oid,hasher='default')
                if user.password == password:
                    request.session['official'] = user.get_official()
                    return redirect('/official_app/main')
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        'Invalid Password!',
                        extra_tags='alert alert-warning alert-dismissible fade show my-3'
                    )
                    return redirect('/official_auth/login')
            else:
                messages.add_message(
                        request,
                        messages.ERROR,
                        'Account Not Found',
                        extra_tags='alert alert-danger alert-dismissible fade show my-3'
                    )
                return redirect('/official_auth/login')
    else:
        form = Login_form()

    context = {
        'form':form
    }

    return render( request, 'official_auth/login.html', context  )