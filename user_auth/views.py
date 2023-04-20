from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            print('username not found')
            messages.info(request, 'invalid username')
            return redirect('user_login')
        
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'incorrect password')
            return redirect('user_login')
    return render(request,'user_auth/login.html')

def user_signup(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        valid = True
        if User.objects.filter(username=username):
            messages.info(request, "Username already exist!")
            valid = False
        if len(username)<4:
            messages.info(request, "Username must be greater than 3 charcters!!")
            valid = False
        if len(username)>20:
            messages.info(request, "Username must be under 20 charcters!!")
            valid = False
        if not username.isalnum():
            messages.info(request, "Username must be alpha numric")
            valid = False
        if len(pass1) < 8:
            messages.warning(request, "Passwords must be altleast 8 characters!!")
            valid = False
        if pass1.isalpha():
            messages.warning(request, "Passwords must contain alteast one number!!")
            valid = False
        if pass1.isalnum():
            messages.warning(request, "Passwords must contain one special character!!")
            valid = False
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            valid = False
        if not valid:
            return redirect('user_signup')

        usr = User.objects.create_user(username = username,password = pass1)
        usr.save()
        return redirect('user_login')

    return render(request,'user_auth/register.html')

@login_required(login_url='user_login')
def user_logout(request):
    logout(request)
    return redirect('user_login')
