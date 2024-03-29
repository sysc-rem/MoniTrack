# views.py
from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import CustomUserCreationForm, UpdateCustomUserForm
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib import messages
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out  # Import user_logged_out signal


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # print(request.POST)
            # print(form.errors)

            login(request, user)  # Redirect to a success page
            create_session(request.user)
            return redirect('/home')
    else:
        form = CustomUserCreationForm()
    # print(form.errors)
    # print(request.POST)
    return render(request, 'registration/sign_up.html', {'form': form})


def home(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect('/user')

    return render(request, 'home/home.html')


def log_in(request):

    login_failed = False
    if request.user.is_authenticated:
        return HttpResponseRedirect('/user')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(f"Logging in {user}")
            login(request, user)

            error_message = create_session(request.user)

            if error_message:
                # messages.error(request, error_message)
                print(f"Error creating session: {error_message}")
            else:
                print("Session created successfully")

            return redirect('/user')
        else:
            login_failed = True  # Set the variable if login fails
            print("Authentication failed")
    return render(request, 'registration/login.html', {'login_failed': login_failed})


def user(request):

    if request.user.is_authenticated:

        session = UserSession.objects.filter(
            user=request.user, logout_time__isnull=True).last()
        user_session = UserSession.objects.filter(
            user=request.user, logout_time__isnull=True).last()
        context = {

            'login_date': session.login_time if session else None,
            'user_session': user_session,
        }
        return render(request, 'home/user.html', context)
    return redirect("/")


# def log_out(request):
#     print(f"Signning out the {request.user}")
#     if request.user.is_authenticated:
        
#         update_session(request.user)  # Update the session record
#         logout(request)

#     return redirect('/logout')


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UpdateCustomUserForm(request.POST, instance=request.user)
            if form.is_valid():
                

                # Use a different variable name to hold the user instance
                current_user = request.user  # Clearer variable name for clarity
                previous_student_number = request.user.student_number
                previous_section = request.user.section
                previous_first_name = request.user.first_name
                previous_last_name = request.user.last_name
                UserRecord.objects.create(
                    user=current_user, previous_student_number=previous_student_number,
                    previous_section=previous_section, previous_first_name=previous_first_name,
                    previous_last_name=previous_last_name)
                form.save()
                messages.success(request, "User Has Been Updated!")
                return redirect('/profile')
        else:
            form = UpdateCustomUserForm(instance=request.user)
    else:
        return redirect('/user')

    return render(request, 'home/profile.html', {'form': form})


def feedback(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST.get('message')

            # Create a new Feedback instance with the retrieved message
            new_feedback = Feedback(user=request.user, message=message)

            # Save the new feedback instance to the database
            new_feedback.save()

            # Success message or redirect (optional)
            # messages.success(request, 'Feedback submitted successfully!')  # Using Django messages framework
            return redirect('home')  # Redirect to another page (e.g., home page)

    return render(request, 'home/feedback.html')

def session_update(request):
    update_session(request.user)