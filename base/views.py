from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Room,Topic,Message
from .forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
# rooms=[
#     {'id':1,'name':'lets learn python'},
#     {'id':2,'name':'design with me'},
#     {'id':3,'name':'frontend developers'},
# ]

classify=[
    {'id':1,'request':'request', 'data':"data",'schema':"schema",'status':"status",'date':"date",'output':'output', 'user':"user"},
    {'id':1,'request':'request', 'data':"data",'schema':"schema",'status':"status",'date':"date",'output':'output', 'user':"user"}

]

def test(request):
    return render(request,'login.html')

def testDash(request):
    return render(request,'home.html')

def testClassify(request):
    return render(request,'classification.html',{'classify':classify})

def testSummary(request):
    return render(request,'summary.html')

def testLibrary(request):
    return render(request,'library.html')

def testSetting(request):
    return render(request,'setting.html')

def testLogin(request):
    return render(request,'loginPage.html')


def loginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist')
    context={'page': page}
    # return render(request,'base/login_register.html',context)
    return render(request,'loginPage.html',context)

    


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form=UserCreationForm()

    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registeration')
    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )
    room_count=rooms.count()
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))


    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render(request,'base/home.html',context)

def room(request,pk):
    room= Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method =='POST':
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url='login')
def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save() 
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('only host can make changes!!')

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room=""

    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('only host can make changes!!')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

@login_required(login_url='login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('only host can make changes!!')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})

@login_required(login_url='login')
def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)