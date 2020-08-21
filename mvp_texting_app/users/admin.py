from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from mvp_texting_app.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()



@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    
    fieldsets = (
        ( "User", {"fields": ("username","email",)} ),
    ) 
    list_display = ("id", "username", "is_staff", "is_active", 
        "is_superuser", "last_deactivated", "email",)
    search_fields = ("id", "username","email",)
    ordering = ('username',)

