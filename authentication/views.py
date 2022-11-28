from base64 import urlsafe_b64encode
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Web_Application import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
#from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template import loader



# Call the app from cmd: python manage.py runserver

# Views 
def home(request): # Create application opening page
    return render(request, "authentication/index.html")

def signup(request): # Create signup form

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        date = request.POST['date']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "This username is already exist! Please try an another one.")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "This email is already registered!")
            return redirect('signup')

        if len(username)>12:
            messages.error(request, "Username cannot excess 12 characters!")
            return redirect('signup')

        if pass1 !=pass2:
            messages.error(request, "Passwords don't match!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        #myuser.is_active = False
        myuser.save()

        messages.success(request, "Your account is successfully created!") # + A confirmation E-mail has been sent to your E-mail adress. To activate your account, please confirm your E-mail. ")

        # Email Confirmation


        #subject = "Welcome to Socall!"
        #message = "Hello " + myuser.username + "!! \n" + "Welcome to Socall! \n Enjoy your time during the visit of our website! \n A confirmation E-mail has been sent to your E-mail adress. To activate your account, please confirm your E-mail. \n\n Best Regards \n Socall Application"
        #from_email = settings.EMAIL_HOST_USER
        #to_list = [myuser.email]
        #send_mail(subject, message, from_email, to_list, fail_silently = True)

        #current_site = get_current_site(request)
        #email_subject = "Please confirm your E-mail to login Socall Application!"
        #message2 = render_to_string('email_confirmation.html'), {'name': myuser.first_name, 'domain': current_site.domain, 'uid': urlsafe_b64encode(force_bytes(myuser.pk)),
        #'token': generate_token.make_token(myuser) })
        #email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [myuser.email])
        #email.fail_silently = True
        #email.send()

        return redirect("signin")

    return render(request, "authentication/signup.html") # Call the form from signup.html file

def signin(request): # Create login functionality

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.username
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Please enter a valid username or password!")
            return redirect('home')

    return render(request, "authentication/signin.html") # Call the form from login.html file

def signout(request): # Create logout functionality
    logout(request)
    messages.success(request, "You logged out successfully!")    
    return redirect('home')

def setprofile(request): # Create user profile
    if request.method == 'POST':
        return redirect('home')
    messages.success(request, "Your profile is successfully set!")    
    return render(request, "authentication/setprofile.html") # Call the form from login.html file

def profile(request): # user profile
    if request.method == 'POST':
        return redirect('home')
    return render(request, "authentication/profile.html") # Call the form from login.html file

    
#def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'activation_failure.html')
