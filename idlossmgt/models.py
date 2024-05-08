from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
#from .models import LostID

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    profile_picture = models.ImageField(_('profile picture'), upload_to='profile_pics/', blank=True, null=True)  # New field
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    email_confirmed = models.BooleanField(_('email confirmed'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


#lost id table
class LostID(models.Model):
    CATEGORY_CHOICES = [
        ('staff', 'Staff ID'),
        ('student', 'Student ID'),
    ]

    hall = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    id_no = models.CharField(max_length=100)
    names = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    phone = models.CharField(max_length=20)
    city_state = models.CharField(max_length=100)
    street_locality = models.CharField(max_length=100)
    date = models.DateField()
    id_picture = models.ImageField(upload_to='lost_id_pictures/', null=True, blank=True)  # Add an image field for ID pictures

    def __str__(self):
        return self.names 

#found ids table
class FoundID(models.Model):
    hall = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    id_no = models.CharField(max_length=100)
    names = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=LostID.CATEGORY_CHOICES)  # Use the choices from LostID model
    description = models.TextField()
    phone = models.CharField(max_length=20)
    city_state = models.CharField(max_length=100)
    street_locality = models.CharField(max_length=100)
    date = models.DateField()
    id_picture = models.ImageField(upload_to='found_id_pictures/', null=True, blank=True)
    found_date = models.DateField(auto_now_add=True)
    found_by = models.CharField(max_length=255)

    def __str__(self):
        return self.names
        


#found and drafted ids
class FoundanddraftedID(models.Model):
    lost_id = models.ForeignKey(LostID, on_delete=models.CASCADE)
    # Fields similar to LostID
    hall = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    id_no = models.CharField(max_length=100)
    names = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=LostID.CATEGORY_CHOICES)  # Use the choices from LostID model
    description = models.TextField()
    phone = models.CharField(max_length=20)
    city_state = models.CharField(max_length=100)
    street_locality = models.CharField(max_length=100)
    date = models.DateField()
    id_picture = models.ImageField(upload_to='found_id_pictures/', null=True, blank=True)
    found_date = models.DateField(auto_now_add=True)
    found_by = models.CharField(max_length=255)

    def __str__(self):
        return self.names
        