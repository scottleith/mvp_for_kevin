from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from mvp_texting_app.persons.models import (
    Person,
    PersonLocation,
    PersonPhone,
    PersonName,
    PersonTraits,
    PersonTextAvailability,
)
from mvp_texting_app.persons.forms import PersonChangeForm

User = get_user_model()

class UserInline(admin.StackedInline):
    model = User
    extra = 1
    fields = ['username','email']

class PersonNameInline(admin.StackedInline):
    model = PersonName
    fields = ['first_name','last_name','preferred_name']
    extra = 0

class PersonPhoneInline(admin.StackedInline):
    model = PersonPhone
    fields = ['phone_number']
    extra = 1

class PersonLocationInline(admin.StackedInline):
    model = PersonLocation
    fields = ['timezone']
    extra = 1

class PersonTraitsInline(admin.StackedInline):
    model = PersonTraits
    fields = ['birth_date','weight_lbs', 'height_inches','gender']
    extra = 0

class PersonTextAvailabilityInline(admin.StackedInline):
    model = PersonTextAvailability
    fields = ['day_type','specific_date','off_limits','start_time','end_time']
    extra = 0

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """
    The central admin for a person. Includes all Person-related tables.

    Contains phone, location, name, traits (e.g., gender), and texting
    availability. List display has id and username ("their_username").
    """
    model = Person
    form = PersonChangeForm

    inlines = [
        UserInline, 
        PersonPhoneInline, 
        PersonLocationInline, 
        PersonNameInline, 
        PersonTraitsInline, 
        PersonTextAvailabilityInline,
    ]

    def their_username(self, obj):
            return User.objects.get(person_id = obj.id).username

        
    their_username.short_description = _("Username")
    list_display = ("id", "their_username",)
    search_fields = ("id",  )
    ordering = ('id',)

   
