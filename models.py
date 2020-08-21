import random
from datetime import datetime as dt

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from mvp_texting_app.texts.models import TextDetails
from mvp_texting_app.schedules.models import TextBooking
from mvp_texting_app.persons.models import PersonTextAvailability
from mvp_texting_app.programs.helpers import add_time_to_date

User = get_user_model()

class TextingProgram(models.Model):
    """
    A texting program is a set schedule of texts. First send this on this date,
    then X days later send this, then Y days later ...
    """
    id = models.AutoField(primary_key = True)
    name = models.CharField(_("texting program name"),
        max_length = 255, help_text = "Name of Texting Program")
    n_texts = models.PositiveIntegerField(_("number of texts in texting program"),
        blank = True, null = True) 
    runtime_days = models.PositiveIntegerField(_("texting program runtime in days"),
        blank = True, null = True) 

    class Meta:
        verbose_name = "Texting Program"
        verbose_name_plural = "Texting Programs"

    def __str__(self):
        return "Name: %s\n Runtime (days): %s\n Number of Texts: %s" %\
            (self.name, self.runtime_days, self.n_texts)

    def save(self, *args, **kwargs):
        if not self.n_texts:
            pass
        if not self.runtime_days:
            pass
        super().save()


class TextingProgramSchedule(models.Model):
    """
    The texts to send, in what order.
    """
    id = models.AutoField(primary_key = True)
    program_id = models.ForeignKey(TextingProgram, on_delete = models.CASCADE)
    text_id = models.ForeignKey(TextDetails, on_delete = models.CASCADE)
    position = models.PositiveIntegerField(
        _("text position in program sequence"),
        help_text = "text position in program sequence: first, second, ...",
        null = False, blank = False)
    delta_days = models.PositiveIntegerField(
        _("Days from Program Start"), help_text = "Days from Program Start",
        null = False, blank = False) 

    class Meta:
        verbose_name = "Program Texts and Order"
        verbose_name_plural = "Programs' Texts and Order"
    
    def __str__(self):
        return "Program: %s\n Text: %s\n Position: %s\n Delta: %s" %\
            (self.program_id, self.text_id, self.position, self.delta_days)



class TextingProgramParticipantRecord(models.Model):
    """
    A record for a given user's participation in a given program.
    """
    id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    program_id = models.ForeignKey(TextingProgram, on_delete = models.CASCADE)
    start = models.DateField(_("The date the user starts the program"))
    end = models.DateField(_("The user's intended end date for the program"))
    active = models.BooleanField(_("Is the user currently on this program?"),
        default = True)
    abandoned = models.BooleanField(
        _("Did the user quit permanently before competion?"),
        null = True, default = models.SET_NULL
        )

    def __str__(self):
        return "User: %s\nProgram: %s,Active: %s\n Start: %s\n, End: %s" %\
            (self.user_id, self.program_id, self.active, self.start, self.end)

    def apply_avail_and_schedule(self, text_id, curr_date, avail_list):
        """
        Given a date and text, schedules the text on the next available
        time in the user's availability.
        """
        num_periods = len(avail_list)
        # If someone has more than one availability block, 
        # choose one at random to feed into the booking process.
        choice = random.randint(0,num_periods-1)
        start = add_time_to_date( curr_date, avail_list[choice].start_time ) 
        end = add_time_to_date( curr_date, avail_list[choice].end_time ) 
        TextBooking.objects.create(
            user_id = self.user_id,
            text_id = text_id,
            start_send_period = start,
            end_send_period = end,
            program_id = self.program_id
        )
    
    def schedule_text_for_user(self, text_id, curr_date, avail_list):
        """
        This function schedules a text intended for the current date,
        sometime inside the next available time period. 
        
        Process:
            - If there is a specific availability for curr_day, we book based 
                on that.
            - If no specific availability, we go to anything day-specific like,
                "I'm available Mondays 10am to 2pm".
            - If no day-specific availability, we just go with the person's default
                "I'm generally good between 6am and 6pm". 
            - The DEFAULT default is 8am to 10pm.
        Example:
            - The current day is Monday Aug 17, but you are unavailable on Aug 17.
            - We move to the next day.
            - The current day is Tuesday.
            - You have no specific notes on Tuesday, but are generally available
                between 6am and 8am, and between 5pm and 10pm.
            - We randomly choose the second opening, and feed the corresponding
                start and end times into the TextBooking object.
        """
        sp = avail_list.filter(specific_date = curr_date)
        gen = avail_list.filter(day_type = curr_date.strftime("%a"))
        default = avail_list.filter(day_type = "General")
        if sp:
            self.apply_avail_and_schedule(
                text_id = text_id, curr_date = curr_date, avail_list = sp
                )
        elif gen:
            self.apply_avail_and_schedule(
                text_id = text_id, curr_date = curr_date, avail_list = gen
                )
        else:
            self.apply_avail_and_schedule(
                text_id = text_id, curr_date = curr_date, avail_list = default
                )
    
    def save(self, *args, **kwargs):
        """
        Happens when someone is signed up for a new program.

        Creates a new text booking for every text in the program, starting with
        the ProgramParticipantRecord start date. Text timing is adjusted
        according to the user's texting preferences.
        
        If a whole day is off-limits, the text is shunted to the next available
        day.
        """
        curr_date = self.start
        pers_id = User.objects.get(id = self.user_id).person_id
        texts = TextingProgramSchedule.objects\
                .get(program_id = self.program_id)\
                .order_by('position')

        for text in texts:
            tid = text.text_id
            curr_date = curr_date + dt.timedelta(days = text.start_delta_days)
            avail_list = PersonTextAvailability.objects.get(person_id = pers_id)
            self.schedule_text_for_user(tid, curr_date, avail_list)
        
        super().save()




