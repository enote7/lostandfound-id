from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignupForm, LoginForm, FoundIDForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


# SIGNUP

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if len(password1) < 8:
                form.add_error('password1', 'Password must be at least 8 characters long.')
            elif password1 != password2:
                form.add_error('password2', 'Passwords do not match.')
            else:
                user.set_password(password1)
                user.save()
                send_confirmation_email(request, user)  # Send confirmation email
                messages.success(request, 'Please check your email to confirm your account.')
                return redirect('login')
        else:
            form.add_error(None, 'Please correct the errors below.')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def send_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    confirmation_link = request.build_absolute_uri(reverse('confirm_email', kwargs={'uidb64': uidb64, 'token': token}))
    subject = 'Confirm your email address'
    message = f"Please click the following link to confirm your email address: {confirmation_link}"
    send_mail(subject, message, 'enote7y@gmail.com', [user.email])


from django.contrib import messages  # Make sure to import messages
 
# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.email_confirmed:
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, 'Please confirm your email address to log in.')
            else:
                # Pass error message to the form
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# EMAIL CONFIRMATION
def confirm_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return render(request, 'email_confirmed.html')
    else:
        return render(request, 'email_confirmation_invalid.html')

def email_confirmation(request):
    return render(request, 'confirmation_email.html')

def email_confirmed(request):
    return render(request, 'email_confirmed.html')

def email_confirmation_invalid(request):
    return render(request, 'email_confirmation_invalid.html')

# PASSWORD RESET
def send_password_reset_email(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'User with this email does not exist.')
        return None

    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
    email_subject = 'Password Reset'
    email_body = render_to_string('password_reset_email.html', {'reset_url': reset_url})
    send_mail(email_subject, email_body, 'enote7y@gmail.com', [email])


from django.shortcuts import render
from .models import FoundID, FoundanddraftedID, LostID
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import JsonResponse
from .models import FoundanddraftedID

@login_required
def home(request):
    # Query the FoundanddraftedID model to get all instances
    found_ids = FoundID.objects.all()
    return render(request, 'home.html', {'found_ids': found_ids})

@login_required
def search_id(request):
    if request.method == 'GET':
        id_number = request.GET.get('id_number')
        try:
            found_id = FoundanddraftedID.objects.get(id_no=id_number)
            data = { 
                'success': True,
                'id_details': {
                    'hall': found_id.hall,
                    'program': found_id.program,
                    'reg_no': found_id.reg_no,
                    'id_no': found_id.id_no,
                    'names': found_id.names,
                    'category': found_id.get_category_display(),
                    'description': found_id.description,
                    'phone': found_id.phone,
                    'city_state': found_id.city_state,
                    'street_locality': found_id.street_locality,
                    'date': found_id.date.strftime('%Y-%m-%d'),
                    'id_picture': found_id.id_picture.url if found_id.id_picture else None,
                    'found_date': found_id.found_date.strftime('%Y-%m-%d'),
                    'found_by': found_id.found_by,
                }
            }
        except FoundanddraftedID.DoesNotExist:
            data = {'success': False}
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request method'})



def success (request):
    return render(request, 'success.html')


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.email_confirmed:
                    login(request, user)
                    return redirect('home')  # Assuming 'home' is the name of your home page URL
                else:
                    form.add_error(None, 'Please confirm your email address to log in.')
            else:
                # Pass error message to the form
                form.add_error(None, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})



def csrf_failure_view(request, reason=""):
    return render(request, 'csrf_failure.html', {'reason': reason})


#Lost id view logic
from .forms import LostIDForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

@login_required  # Ensure user is logged in to access this view
def lostid(request):
    if request.method == 'POST':
        form = LostIDForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            lost_id = form.save()
            # Sending email to superuser
            subject = 'New Lost ID Submitted'
            message = f"A new lost ID has been submitted. ID: {lost_id.id}"
            sender_email = request.user.email  # Get the email address of the logged-in user
            superusers = CustomUser.objects.filter(is_superuser=True)
            recipients = [admin.email for admin in superusers]
            send_mail(subject, message, sender_email, recipients, fail_silently=True)
            messages.success(request, 'Lost ID submitted successfully.')
            return redirect('success')  # Redirect to the home page after successful submission with a success message
    else:
        form = LostIDForm()
    return render(request, 'lostid.html', {'form': form})



#found id view logic
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

@login_required  # Ensure user is logged in to access this view
def foundid(request):
    if request.method == 'POST':
        form = FoundIDForm(request.POST, request.FILES)
        if form.is_valid():
            found_id = form.save()
            # Sending email to superuser
            subject = 'New Found ID Submitted'
            message = f"A new found ID has been submitted. ID: {found_id.id}"
            sender_email = request.user.email  # Get the email address of the logged-in user
            superusers = CustomUser.objects.filter(is_superuser=True)  # Use CustomUser model
            recipients = [admin.email for admin in superusers]
            send_mail(subject, message, sender_email, recipients, fail_silently=True)
            messages.success(request, 'Found ID submitted successfully.')
            return redirect('success')  # Redirect to the home page after successful submission with a success message
    else:
        form = FoundIDForm()
    return render(request, 'foundid.html', {'form': form})





from django.shortcuts import render
from .models import FoundanddraftedID

@login_required
def found_and_drafted_ids(request):
    found_and_drafted_ids = FoundanddraftedID.objects.all()
    return render(request, 'found_and_drafted_ids.html', {'found_and_drafted_ids': found_and_drafted_ids})

from django.http import JsonResponse


    
@login_required
def lid_view(request):
    lost_ids = LostID.objects.all()
    return render(request, 'lid.html', {'lost_ids': lost_ids})


@login_required
def fid_view(request):
    found_ids = FoundID.objects.all()
    return render(request, 'fid.html', {'found_ids': found_ids})


@login_required
def about_us(request):
    team_members = [
        {'name': 'Nantege Sanyu Annet', 'image': 'as1.jpg'},
        {'name': 'Arinaitwe Precious', 'image': 'as2.jpg'},
        {'name': 'Akamusiima Siifa', 'image': 'as3.jpg'},
        {'name': 'Mathias Lubanjwa', 'image': 'as4.jpg'},
    ]
    return render(request, 'about_us.html', {'team_members': team_members})
