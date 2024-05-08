from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import CustomUser, LostID, FoundID, FoundanddraftedID

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'email_confirmed', 'profile_picture')  
    search_fields = ('email', 'first_name', 'last_name')  
    readonly_fields = ('last_login',)  

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ('Email Confirmation', {'fields': ('email_confirmed',)}),  
        ('Important dates', {'fields': ('last_login',)}),
        ('Profile Picture', {'fields': ('profile_picture',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser', 'email_confirmed', 'profile_picture')}  
        ),
    )
    ordering = ('first_name',)  # Update ordering to first_name

admin.site.register(CustomUser, CustomUserAdmin)

# Register LostID model
@admin.register(LostID)
class LostIDAdmin(admin.ModelAdmin):
    list_display = ('hall', 'program', 'reg_no', 'id_no', 'names', 'category', 'phone', 'city_state', 'street_locality', 'date', 'id_picture')
    search_fields = ('hall', 'program', 'reg_no', 'id_no', 'names', 'phone', 'city_state', 'street_locality', 'id_picture')
    list_filter = ('hall', 'program', 'category')

#register found id
@admin.register(FoundID)
class FoundIDAdmin(admin.ModelAdmin):
    list_display = ('hall', 'program', 'reg_no', 'id_no', 'names', 'category', 'phone', 'city_state', 'street_locality', 'date', 'id_picture')
    search_fields = ('hall', 'program', 'reg_no', 'id_no', 'names', 'phone', 'city_state', 'street_locality', 'id_picture')
    list_filter = ('hall', 'program', 'category')


#register found and drafted ids
@admin.register(FoundanddraftedID)
class FoundanddraftedIDAdmin(admin.ModelAdmin):
    list_display = ('hall', 'program', 'reg_no', 'id_no', 'names', 'category', 'phone', 'city_state', 'street_locality', 'date', 'id_picture')
    search_fields = ('hall', 'program', 'reg_no', 'id_no', 'names', 'phone', 'city_state', 'street_locality', 'id_picture')
    list_filter = ('hall', 'program', 'category')