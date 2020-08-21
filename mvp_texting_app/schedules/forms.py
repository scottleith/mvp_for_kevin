from django import forms

from mvp_texting_app.schedules.models import TextBooking, GoalSchedule

class TextBookingCreationForm(forms.ModelForm):

    class Meta:
        model = TextBooking
        fields = ['user_id', 'text_id', 'start_send_period', 'end_send_period']


class TextBookingChangeForm(forms.ModelForm):

    class Meta:
        model = TextBooking
        fields = ['user_id', 'text_id', 'start_send_period', 'end_send_period']


class GoalScheduleCreationForm(forms.ModelForm):

    class Meta:
        model = GoalSchedule
        fields = [
            'user_id', 
            'goal_name', 'goal_description',
            'start', 'end'
            ]


class GoalScheduleChangeForm(forms.ModelForm):

    class Meta:
        model = GoalSchedule
        fields = [
            'user_id', 
            'goal_name', 'goal_description',
            'start', 'end'
            ]