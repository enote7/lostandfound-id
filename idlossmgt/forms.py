from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


# Signup Form
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    confirmation_token = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
# LOGIN
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

#USER MODEL
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',)


#password reset
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')


from django import forms
from .models import LostID, FoundID

class LostIDForm(forms.ModelForm):
    class Meta:
        model = LostID
        fields = ['hall', 'program', 'reg_no', 'id_no', 'names', 'category', 'description', 'phone', 'city_state', 'street_locality', 'date', 'id_picture']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
            'hall': forms.TextInput(attrs={'placeholder': 'if staff put "none"'}),
            'program': forms.TextInput(attrs={'placeholder': 'if staff put "none"'}),
            'reg_no': forms.TextInput(attrs={'placeholder': 'Registration Number'}),
            'id_no': forms.TextInput(attrs={'placeholder': 'ID Number'}),
            'names': forms.TextInput(attrs={'placeholder': 'Names'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description of the ID'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'city_state': forms.TextInput(attrs={'placeholder': 'City/State'}),
            'street_locality': forms.TextInput(attrs={'placeholder': 'Street/Locality'}),
            'id_picture': forms.FileInput(),  # Use FileInput widget for the id_picture field
        }

class FoundIDForm(forms.ModelForm):
    class Meta:
        model = FoundID
        fields = ['hall', 'program', 'reg_no', 'id_no', 'names', 'category', 'description', 'phone', 'city_state', 'street_locality', 'date', 'id_picture']
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'MM/DD/YYYY'}),
                'hall': forms.TextInput(attrs={'placeholder': 'if staff put "none"'}),
                'program': forms.TextInput(attrs={'placeholder': 'if staff put "none"'}),
                'reg_no': forms.TextInput(attrs={'placeholder': 'Registration Number'}),
                'id_no': forms.TextInput(attrs={'placeholder': 'ID Number'}),
                'names': forms.TextInput(attrs={'placeholder': 'Names'}),
                'description': forms.Textarea(attrs={'placeholder': 'Description of the ID'}),
                'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
                'city_state': forms.TextInput(attrs={'placeholder': 'City/State'}),
                'street_locality': forms.TextInput(attrs={'placeholder': 'Street/Locality'}),
                'id_picture': forms.FileInput(),  # Use FileInput widget for the id_picture field
            }


#found and drafted id
class FoundanddraftedIDForm(forms.ModelForm):
    class Meta:
        model = FoundID
        fields = ['hall', 'program', 'reg_no', 'id_no', 'names', 'category', 'description', 'phone', 'city_state', 'street_locality', 'date', 'id_picture']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }