from django.shortcuts import render, redirect
from django.template import Template , Context
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.contrib import messages
from agenda.forms import *
from django.contrib.auth.decorators import login_required
from agenda.models import Events
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
 #       import pdb;pdb.set_trace()
        if form.is_valid():
            users = User(
                username=form.cleaned_data['username'],
                password=make_password(form.cleaned_data['password1']),
                is_staff=False,
                is_active=True,
                is_superuser=False,
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            try:
                users.full_clean()
            except ValidationError as e:
                pass

            try:
                validate_password(form.cleaned_data['password1'], user=None, password_validators=None)
            except ValidationError as e:
                form.add_error('password1', e)  # to be displayed with the field's errors
                return render(request, 'register.html', {'form': form})


            users.save()
            messages.success(request, 'Member was created successfully!')
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def register_success(request):
    return render(request, 'success.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def agenda(request):
    return render(request, 'agenda.html')

@login_required
def createevent(request):
    if request.method == 'POST':
        myid = request.POST['id']
        if myid:
            data = Events.objects.get(id=myid)
            data.title = request.POST['title']
            data.description = request.POST['description']
            data.start_time = request.POST['start_time']
            data.end_time = request.POST['end_time']
        else:
            data = Events(
                title=request.POST['title'],
                description=request.POST['description'],
                start_time=request.POST['start_time'],
                end_time=request.POST['end_time'],
            )
        data.save()
        return JsonResponse({'data': 'success'})

@login_required
def getevents(request):
    if request.method == 'GET':
        events = Events.objects.all()
        event_list = []
        for event in events:
            event_list.append(
                {
                    "id": event.id,
                    "title": event.title,
                    "start": event.start_time,
                    "end": event.end_time,

                }
            )

        return JsonResponse(event_list, safe=False)
    else:
        return JsonResponse({'data': 'failure'})
    
@login_required
def editevent(request):
    event_id = request.POST['id']
    event = Events.objects.get(id=event_id)
    event_dict = {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "start": event.start_time,
        "end": event.end_time,
    }
    return JsonResponse(event_dict, safe=False)
    
@login_required
def deleteevent(request):
    id = request.POST['id']
    event = Events.objects.get(id=id)
    event.delete()
    return JsonResponse({'event': 'success'})

@login_required
def profile(request):
    return render(request, 'profile.html')

@csrf_protect
def saveprofile(request, id):
    data = User.objects.get(id=id)
    data.first_name = request.POST['first_name']
    data.last_name = request.POST['last_name']
    data.email = request.POST['email']
    if request.POST['password']:
        data.password = password=make_password(request.POST['password'])
    data.save()
    messages.success(request, "Dati salvati con successo.")
    return redirect('/profile')

@login_required
def users(request):    
    return render(request, 'users.html', {'users': users})

@csrf_protect
def ausers(request):
    result_list = list(User.objects.all()\
                .values('id',
                        'username',
                        'first_name',
                        'last_name',
                        'email',
                        'is_staff',
                       ))  
    return JsonResponse(result_list, safe=False)

@csrf_protect
def storeuser(request):
    myid = request.POST['id']
    if myid:
        data = User.objects.get(id=myid)
        data.username = request.POST['username']
        data.first_name = request.POST['first_name']
        data.last_name = request.POST['last_name']
        data.email = request.POST['email']
        data.is_staff = request.POST['is_staff']
        if request.POST['password']:
            data.password = password=make_password(request.POST['password'])
        data.save()
    else:
        data = User(
                username=request.POST['username'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                is_staff=request.POST['is_staff'],
                password=make_password(request.POST['password']),
            )
        data.save()
    return JsonResponse({'data': 'success'})


@csrf_protect
def edituser(request, id):
    member = User.objects.get(id=id)
    member_dict = {
        "id": member.id,
        "username": member.username,
        "first_name": member.first_name,
        "last_name": member.last_name,
        "email": member.email,
        "is_staff": member.is_staff,
    }
    return JsonResponse(member_dict, safe=False)

@login_required
def deleteuser(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return JsonResponse({'user': 'success'})


