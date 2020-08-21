import datetime as dt
import random

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel

from mvp_texting_app.texts.models import TextDetails
from mvp_texting_app.persons.models import Person, PersonLocation
from mvp_texting_app.schedules.helpers import convert_to_utc, change_tz_only

User = get_user_model()


class GoalSchedule(TimeStampedModel):

    class Meta:
        app_label = 'schedules'
        verbose_name = "User Goal Schedule"
        verbose_name_plural = "User Goal Schedules"

    id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    goal_name = models.CharField("Goal Description", max_length = 140, blank = True, null = True)
    goal_description = models.TextField("Goal Description", blank = True, null = True)
    start = models.DateField("Goal Schedule Start Date")
    end = models.DateField("Goal Schedule End Date", blank = True)

    def __str__(self):
        return self.goal_name

    def set_name(self, name):
        self.goal_name = name

    def get_description(self):
        return self.goal_description

    def set_description(self, description):
        self.goal_description = description



class TextBooking(TimeStampedModel):

    class Meta:
        app_label = 'schedules'
        verbose_name = "Text Booking"
        verbose_name_plural = "Text Bookings"

    id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    goal_schedule_id = models.ForeignKey(GoalSchedule, null = True, blank = True,
        on_delete = models.CASCADE)
    text_id = models.ForeignKey(TextDetails, on_delete = models.CASCADE)
    
    start_send_period = models.DateTimeField(null = False, blank = False)
    end_send_period = models.DateTimeField(null = False, blank = False)
    final_send_dt = models.DateTimeField(blank = True, null = False)
    
    #objects = UserTextingScheduleManager()

    def __str__(self):
        return "User: %s\nText: %s\nSend Time: %s" % \
            ( self.user_id, self.text_id, self.final_send_dt )

    def save(self, *args, **kwargs):
        """
        Handles random time assignment and user timezone. Example:

        1. They tell us in chat that they want a text between 6pm and 8pm.
        2. We use the form to input 6pm start, 8pm end. Both are assigned the 
            default UTC, which is not local time for the user.
        3. To correct this, we: 
            - Calculate the final send time, also in UTC (e.g., 6:30pm UTC).
            - Change the default UTC os start/end/final to the user's local tz.
              This gives us 6pm/8pm/630pm, user's local tz.
            - Convert these correct times to UTC and store in the database.
        """
        
        assert isinstance(self.start_send_period, dt.datetime)
        assert isinstance(self.end_send_period, dt.datetime)
        assert self.end_send_period >= self.start_send_period
       
       # First we calculate the final send time in UTC
        num_mins = round(
            (self.end_send_period - self.start_send_period).seconds / 60,
            0 
            )
        delta = random.randint(0,num_mins)
        temp_final = self.start_send_period + dt.timedelta(minutes=delta)

        # Then we get the user's local tz, e.g., "US/Eastern"
        pid = User.objects.get(username = self.user_id).person_id
        local_tz = str( PersonLocation.objects.get(person_id = pid).timezone )
            
        print(local_tz)

        # Next we obtain the correct, user-intended local times.
        local_start = change_tz_only( self.start_send_period, local_tz)
        local_end = change_tz_only( self.end_send_period, local_tz )
        local_final = change_tz_only( temp_final, local_tz )
        print(
            "Local Start: %s \n Local End: %s\nLocal Final: %s" % \
            (local_start, local_end, local_final)
        )

        # Then we convert the local times to UTC and save.
        self.start_send_period = convert_to_utc(local_start)
        self.end_send_period = convert_to_utc(local_end)
        self.final_send_dt = convert_to_utc( local_final )
        print("UTC Start: %s \n UTC End: %s\nUTC Final: %s" % \
            (self.start_send_period, self.end_send_period, self.final_send_dt)
        )
        super().save()


class GoalSchedulesBookings_BRIDGE(models.Model):

    id = models.AutoField(primary_key = True)
    goal_schedule_id = models.ForeignKey(GoalSchedule, on_delete = models.CASCADE)
    text_booking_id = models.ForeignKey(TextBooking, on_delete = models.CASCADE)