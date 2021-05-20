
from user_auth.decorators import user_logged_in
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import hashers
from django.contrib import messages

from .forms import register_user,login_user
from .models import User
# Create your views here.
@user_logged_in
def registerUser(request):

    form = register_user()


    if request.method == 'POST':
        form = register_user(data=request.POST)
        print(form.data)
        if form.is_valid():
            data = form.save(commit=False)
            data.name = str.upper(form.cleaned_data['name'])
            data.password = hashers.make_password(form.cleaned_data['password'],salt=form.cleaned_data['uid'],hasher='default')
            data.save()
            user = User.objects.get(uid=form.cleaned_data['uid']).get_user()
            request.session['user'] = user
            return redirect('dashboard')
    
    context = {
            'form':form,
        }

    return render(request, 'user_auth/register.html',context)




@user_logged_in
def loginUser(request):

    form = login_user()

    if request.method == 'POST':
        form = login_user(data=request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(username = request.POST['username'])
            except User.DoesNotExist:
                user = None
            if user:
                password = hashers.make_password(form.cleaned_data['password'],salt=user.uid,hasher='default')
                if user.password == password:
                    user = user.get_user()
                    request.session['user'] = user
                    return redirect('dashboard')
                else:
                    messages.add_message(
                            request,
                            messages.ERROR,
                            'Invalid Password',
                            extra_tags='alert alert-danger alert-dismissible fade show my-3'
                        )
                    return redirect('/user_auth/login')
            else:
                messages.add_message(
                        request,
                        messages.ERROR,
                        'Account Not Found',
                        extra_tags='alert alert-danger alert-dismissible fade show my-3'
                    )
                return redirect('/user_auth/login')
    else:
        form = login_user()
    

    context = {
            'form':form
    }
    return render(request, 'user_auth/login.html',context)

