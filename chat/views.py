import string
from django.shortcuts import render, get_object_or_404,redirect
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import PermissionDenied
# Create your views here.
@login_required(login_url='user_login')
def home(request):
    params = {
        'recived_messages' : Message.objects.filter(receiver = request.user).order_by('-created_at')
    }
    return render(request,'chat/home.html',params)
@login_required(login_url='user_login')
def user(request,username):
    view_user = get_object_or_404(User,username=username)
    if view_user.username == request.user.username:
        view_user_sent_messages = Message.objects.filter(sender = view_user).order_by('-created_at')
    else:
        view_user_sent_messages = Message.objects.filter(sender = view_user,receiver = request.user).order_by('-created_at')

    params = {
        'view_user' : view_user,
        'view_user_sent_messages': view_user_sent_messages,
    }
    return render(request,'chat/user.html',params)

@login_required(login_url='user_login')
def message(request,mid):
    message = Message.objects.filter(pk = mid).first()
    if not((message.receiver.username == request.user.username) or (message.sender.username == request.user.username)):
        raise PermissionDenied
    params= {
        'message' : message
    }
    return render(request,'chat/message.html',params)
@login_required(login_url='user_login')
def new(request):
    if request.method == 'POST':
        reciever = request.POST['reciever']
        title = request.POST['title']
        content = request.POST['content']
        valid = True
        if reciever == '':
            messages.add_message(request,level='230',message='enter the reciver\'s name',extra_tags='reciever_error')
            redirect('new')
        if title == '':
            messages.add_message(request,level='230',message='enter the title',extra_tags='title_error')
            valid = False
        if content == '':
            messages.add_message(request,level='230',message='enter the message',extra_tags='content_error')
            valid = False
        if User.objects.filter(username = reciever).first() is None and reciever != '':
            messages.add_message(request,level='230',message='no such user',extra_tags='reciever_error')
            valid = False
        if not valid:
            redirect('new')
        if valid:
            Message(sender = request.user,receiver= User.objects.filter(username = reciever).first(),title = title,content = content).save()
            redirect('user',username=request.user.username)
    return render(request,'chat/new.html')

@login_required(login_url='user_login')
def profile(request):
    if request.method == "POST":
        if 'username' in request.POST:
            username = request.POST['username']
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
            if not valid:
                return redirect('profile')
            usr = User.objects.filter(username = request.user.username).first()
            usr.username = username
            usr.save()

        elif 'pass1' in request.POST:

            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            valid = True

            if pass1 == '':
                messages.warning(request, "enter old password")
                valid = False
            elif not request.user.check_password(pass1):
                messages.warning(request, "Incorrect Password")
                valid = False
            if pass2 == '':
                messages.error(request, "Enter New Password!!")
                valid = False
            elif len(pass2) < 8:
                messages.error(request, "Passwords must be altleast 8 characters!!")
                valid = False
            if not any(char.isdigit() for char in pass2):
                messages.error(request, "Passwords must contain alteast one number!!")
                valid = False
            if  not any(char in string.punctuation for char in pass2):
                messages.error(request, "Passwords must contain a special character!!")
                valid = False

            if request.user.check_password(pass1) and pass1 == pass2:
                messages.error(request, "New password can't be same as Old password!!")
                valid = False
            if not valid:
                return redirect('profile')
            usr = request.user
            usr.set_password(pass2)
            usr.save()

        elif 'profilepic' in request.FILES:
            if request.FILES['profilepic'] == '':
                messages.add_message(request,level='230',message='no profile pic added',extra_tags='img')
            else:
                new_pfp = request.FILES['profilepic']
                profile = request.user.profile
                profile.profile_pic = new_pfp
                profile.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('profile')

        return redirect('profile')
    return render(request,'chat/profile.html')
