from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from admin_app.models import *
import random
import datetime
from django.utils import timezone
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.utils.timezone import make_aware



# Create your views here.
def home(request):
    user_id = request.session.get("user_id")
    if user_id:
        user = User.objects.get(user_id=user_id)

        total_tasks = Task.objects.filter(user_id=user_id).count()
        total_projects = Project.objects.filter(user_id=user_id).count()
        total_completed_tasks = Task.objects.filter(user_id=user_id, status='done').count()
        total_completed_projects = Project.objects.filter(user_id=user_id, status='done').count()

        recent = Task.objects.all().order_by('-created_at')[:1]
        projects = Project.objects.filter(status='done').order_by('-updated_at')

        context = {
            'user': user,
            'recent': recent,
            'pro': projects,
            'total_tasks': total_tasks,
            'total_projects': total_projects,
            'total_completed_tasks': total_completed_tasks,
            'total_completed_projects': total_completed_projects,
        }

        return render(request, 'index.html', context)
    else:
        return redirect('/login')
def registration(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match.'})
        otp = str(random.randint(100000, 999999))
        otp_created_at = datetime.datetime.now()
        print(firstname, lastname, email, password, phone_number, otp)
        data = User()
        data.firstname=firstname
        data.lastname=lastname
        data.email=email
        data.phone_number=phone_number
        data.password=password
        print('hl')
        data.otp=otp
        data.otp_created_at=otp_created_at
        print('hi')
        data.save()
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            )
        request.session['user_id'] = data.user_id
        return redirect('/otp_verify')
    return render(request, 'registration.html')

def otp_verify(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return render(request, 'otp_verify.html', {'error': 'No user ID found in session.'})

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return render(request, 'otp_verify.html', {'error': 'User does not exist.'})

    if request.method == "POST":
        otp = request.POST.get("otp")

        print(f"Entered OTP: {otp}")
        print(f"Stored OTP: {user.otp}")

        if otp == user.otp:
            otp_age = timezone.now() - user.otp_created_at
            print(f"OTP age: {otp_age}")  # Debugging step
            if otp_age > datetime.timedelta(minutes=10):
                return render(request, 'otp_verify.html', {'error': 'OTP has expired.'})

            # # Activate the user
            # user.is_active = 'Active'
            # user.save()

            # # Clear the session after successful verification
            # del request.session['user_id']

            return redirect('/login')
        else:
            return render(request, 'otp_verify.html', {'error': 'Invalid OTP.'})

    return render(request, 'otp_verify.html')


def request_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                user.otp = otp
                user.otp_created_at = datetime.datetime.now()
                user.save()

                # Send OTP email
                send_mail(
                    'Your OTP Code for Password Change',
                    f'Your OTP code is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent to your email.")
                return redirect('/verify_otps')
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")
        else:
            messages.error(request, "Email is required.")

    return render(request, 'forgotten.html')


def verify_otps(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'verify_otps.html')

        if email and otp:
            try:
                user = User.objects.get(email=email, otp=otp)
                otp_created_at = user.otp_created_at

                if timezone.is_naive(otp_created_at):
                    otp_created_at = make_aware(otp_created_at, timezone.get_current_timezone())

                if timezone.now() - otp_created_at <= datetime.timedelta(minutes=10):
                    user.password = new_password
                    user.otp = otp
                    user.otp_created_at = otp_created_at
                    user.save()

                    messages.success(request, "Password changed successfully.")
                    return redirect('/login')
                else:
                    messages.error(request, "OTP has expired.")
            except User.DoesNotExist:
                messages.error(request, "Invalid OTP or email.")

    return render(request, 'verify_otps.html')
def user_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_data=User.objects.filter(email=email,password=password)
        if user_data:
            for x in user_data:
                id=x.user_id
                request.session['user_id']=id
                return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password.'})
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/login')

def personal_task(request):
    return render(request,'personal_task.html')


def create_personal_task(request):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            status = request.POST.get('status')
            user = User.objects.get(pk=user_id)
            data = Personal_task()
            data.title=title
            data.description=description
            data.status=status
            data.user_id=user
            data.save()

            return redirect('/view_personal_task')
    return render(request, 'add_personal_task.html')

def personal_task_list(request):
    tasks = Personal_task.objects.all()
    return render(request, 'view_personal_task.html', {'tasks': tasks})


def update_personal_task(request, personal_task_id):
    if 'user_id' in request.session:
        user_id = request.session.get("user_id")
        data=Personal_task.objects.filter(personal_task_id=personal_task_id)
        if request.method == "POST":
            title = request.POST.get('title')
            description = request.POST.get('description')
            status = request.POST.get('status')

            user = User.objects.get(pk=user_id)

            data = Personal_task.objects.get(personal_task_id=personal_task_id)
            data.title=title,
            data.description=description,
            data.status=status,
                # users_id=user
            data.save()

            return redirect('/view_personal_task')
    return render(request, 'edit_personal_task.html',{'tasks':data})

def remove_personal_task(request,personal_task_id):
    print("remove fun called")
    data = Personal_task.objects.get(personal_task_id=personal_task_id)
    data.delete()
    return redirect('/view_personal_task')

def assigned_task_list(request):
    # tasks = Personal_task.objects.all()
    return render(request, 'assigned_task.html')


def view_assigned_tasks(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        tasks = Task.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'admin_assigned_task.html', {'tasks': tasks})
    else:
        return redirect('/login')

def team_management(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        team_managements = Team_management.objects.all()
        return render(request, 'team_assigned_task.html', {'team': team_managements})
    else:
        return redirect('/login')


def edit_task_status(request, task_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        task = Task.objects.get( task_id=task_id)
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(Task.STATUS_CHOICES):
                task.status = new_status
                task.updated_at = timezone.now()
                task.save()
                return redirect('/admin_assigned_task')
            else:
                return render(request, 'edit_task.html', {'task': task, 'error': 'Invalid status value.'})

        return render(request, 'edit_task.html', {'task': task})
    else:
        return redirect('/login')

def edit_task(request,task_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        task = Task.objects.get( task_id=task_id)
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(Task.STATUS_CHOICES):
                task.status = new_status
                task.updated_at = timezone.now()
                task.save()
                return redirect('/team_assigned_task')
            else:
                return render(request, 'edit_task.html', {'task': task, 'error': 'Invalid status value.'})

        return render(request, 'edit_task.html', {'task': task})
    else:
        return redirect('/login')
def project(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        tasks = Project.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'project.html', {'project': tasks})
    else:
        return redirect('/login')
def edit_project(request,project_id):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        task = Project.objects.get( project_id=project_id)
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(Project.STATUS_CHOICES):
                task.status = new_status
                task.updated_at = timezone.now()
                task.save()
                return redirect('/project')
            else:
                return render(request, 'edit_project.html', {'task': task, 'error': 'Invalid status value.'})

        return render(request, 'edit_project.html', {'task': task})
    else:
        return redirect('/login')
def profile(request):
    if 'user_id' in request.session:
        user = request.session['user_id']
        data = User.objects.filter(user_id=user)
        return render(request, 'profile.html', {'user': data})
    else:
        return redirect('/login')


def edit_profile(request):
    user_id = request.session.get("user_id")
    if user_id:
        user = User.objects.get(user_id=user_id)
        if request.method == 'POST':
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            phone_number = request.POST.get('phone_number')
            if firstname and lastname and phone_number:
                user.firstname = firstname
                user.lastname = lastname
                user.phone_number = phone_number
                user.updated_at = timezone.now()
                user.save()

                messages.success(request, "Profile updated successfully.")
                return redirect('/profile')
            else:
                messages.error(request, "All fields are required.")

        return render(request, 'edit_profile.html', {'user': user})

def report(request):
    if 'user_id' in request.session:
        user = request.session['user_id']
        tasks = Personal_task.objects.filter(user_id=User.objects.get(user_id=request.session['user_id']))
        return render(request, 'view_personal_task.html', {'tasks': tasks})
    else:
        return redirect('/login')
