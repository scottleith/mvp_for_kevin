
from django.db import models
import datetime as dt
from dateutil.relativedelta import relativedelta

from django_countries.fields import CountryField
from timezone_field import TimeZoneField
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import JSONField
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _


DAY_TYPE_CHOICES = [
        ("Mon", "Monday"),
        ("Tue", "Tuesday"),
        ("Wed", "Wednesday"),
        ("Thu", "Thursday"),
        ("Fri", "Friday"),
        ("Sat","Saturday"),
        ("Sun", "Sunday"),
        ("General", "General"),
        ("Specific", "Specific"),
    ]
def person_model_metadata_json_default_value():
    return {"user_has_metadata": "no"}
    
class Person(TimeStampedModel):
    """
    The central table for Person identity.
    """
    id = models.AutoField(primary_key = True)
    metadata = JSONField(default = person_model_metadata_json_default_value)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return "Person ID: {}".format( self.id )


class PersonTextAvailability(TimeStampedModel):
    """
    The days and times where a person is available to receive texts.
    """
    id = models.AutoField(primary_key = True)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    day_type = models.CharField(max_length = 20, choices = DAY_TYPE_CHOICES)
    specific_date = models.DateField(default = None, null = True, blank = True)
    off_limits = models.BooleanField(default = False)
    start_time = models.TimeField(default = dt.time(9,0,0), \
        null = True, blank = True)
    end_time = models.TimeField(default = dt.time(21,0,0), \
        null = True, blank = True)

    class Meta:
        verbose_name = "Person Text Availability"
        verbose_name_plural = "Peoples' Text Availability"

    def __str__(self):
        return "Person ID: {pid}, Type: {type}"\
            .format(pid = self.person_id, type = self.day_type)


class PersonName(TimeStampedModel):
    id = models.AutoField(primary_key = True)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    first_name = models.CharField(
        _("First Name"), max_length = 100, blank = True, null = True)
    last_name = models.CharField(
        _("Last Name"), max_length = 255, blank = True, null = True)
    preferred_name = models.CharField(
        _("Preferred Name"), max_length = 255, blank=True, null = True)

    class Meta:
        verbose_name = "Person Name"
        verbose_name_plural = "Peoples' Names"

    def __str__(self):
        if self.first_name:
            return "ID: {pid}, First Name: {fn}"\
                .format(pid = self.person_id, fn = self.first_name)
        elif self.preferred_name:
            return "ID: {pid}, First Name: {fn}"\
                .format(pid = self.person_id, fn = self.first_name)
        else:
            return "No first or preferred name in record. ID: {pid}"\
                .format(pid = self.person_id)

    def save(self, *args, **kwargs):
        if not self.preferred_name and self.first_name:
            self.preferred_name = self.first_name
        super().save()


class PersonLocation(TimeStampedModel):
    id = models.AutoField(primary_key = True)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    timezone = TimeZoneField(default = 'UTC')
    country = CountryField() 
    city = models.CharField(null = True, blank = True, max_length = 100)
    address = models.CharField(null = True, blank = True, max_length = 155)
    postal_or_zip = models.CharField(null = True, blank = True, max_length = 7)

    class Meta:
        verbose_name = "Person Location"
        verbose_name_plural = "Peoples' Locations"

    def __str__(self):
        """

        """
        loc_info = [str(self.timezone)]
        if country:
            loc_info.append( str(self.country) )
        if city:
            loc_info.append( str(self.city) )
        return " ".join(loc_info)


class PersonEmail(TimeStampedModel):
    id = models.AutoField(primary_key = True)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    email_address = models.EmailField(
        _('person email address'), blank = True, null = True
        )
    preferred_email = models.BooleanField(default = True)

    class Meta:
        verbose_name = "Person Name"
        verbose_name_plural = "Peoples' Emails"

    def __str__(self):
        if self.preferred_email: 
            x = "Preferred Email"
        else:
            x = "Not Preferred Email"
        return "{pref}: {email}".format(pref = x, email = self.email_address)


class PersonPhone(TimeStampedModel): 
    id = models.AutoField(primary_key = True)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    phone_number = PhoneNumberField("Phone Number", null = False, blank = False, unique = True)
    preferred = models.BooleanField("Preferred/Primary Number", default = True)

    class Meta:
        verbose_name = "Person Phone Number"
        verbose_name_plural = "Peoples' Phone Numbers"
        
    def __str__(self):
        if self.preferred: 
            x = "Preferred Phone Number"
        else:
            x = "Not Preferred Phone Number"
        return "{pref}: {phone}".format(pref = x, phone = self.phone_number)


class PersonTraits(TimeStampedModel):
    """
    A person's demographic and other immutable traits. Age, gender, ...
    """
    id = models.AutoField(primary_key = True)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    birth_date = models.DateField(
        _("Date of Birth"), blank = True, null = True
        )
    age_years = models.PositiveIntegerField(
        _("Age in Years"), null = True, blank = True
        )
    weight_lbs = models.FloatField(null = True, blank = True)
    height_inches = models.FloatField(null = True, blank = True)
    gender_choices = [
        ("M", "Male"),
        ("F", "Female"),
        ("MtF", "Transgender - Male to Female"),
        ("FtM", "Transgender - Female to Male"),
        ("oth", "Other")
    ]
    gender = models.CharField(max_length = 50, blank = True, null = True,
        choices = gender_choices)
    gender_descr = models.CharField(max_length = 255, blank = True, null = True)
    
    class Meta:
        verbose_name = "Person Traits"
        verbose_name_plural = "Peoples' Traits"

    def __str__(self):
        if self.birth_date:
            age = ((dt.datetime.now() - self.birth_date))
            return " ".join( [age, self.gender] )

    def save(self, *args, **kwargs):
        if not self.age_years and self.birth_date:
            # Note that you'll have to check every day to see if it's 
            # someone's birthday. Useful for other reasons too.
            self.age_years = ((dt.datetime.now() - self.birth_date))
        super().save()
