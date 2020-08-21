from django.contrib import admin
from django.contrib.auth import get_user_model

from mvp_texting_app.schedules.models import GoalSchedule, TextBooking
from mvp_texting_app.schedules.forms import (
    GoalScheduleChangeForm, GoalScheduleCreationForm,
    TextBookingChangeForm, TextBookingCreationForm
)
from mvp_texting_app.texts.models import TextDetails

class TextBookingInline(admin.StackedInline):
    """
    Create bookings when you create goals.
    """
    model = TextBooking
    extra = 0

@admin.register(TextBooking)
class TextBookingAdmin(admin.ModelAdmin):
    form = TextBookingChangeForm
    add_form = TextBookingCreationForm
    model = TextBooking

    fieldsets = (
            ("info", 
            {"fields": ("user_id", "goal_schedule_id", "text_id",)}
            ),
            ("time", 
            {'fields': ("start_send_period", "end_send_period", "final_send_dt")}
            ),
        ) 
    list_display = ("id", "user_id", "final_send_dt", "goal_schedule_id",
        "text_id", "start_send_period", "end_send_period", 
        "created", "modified", )
    search_fields = ("id", "user_id", "text_id", 
        "final_send_dt", "goal_schedule_id", "created", )
    ordering = ('id',)


@admin.register(GoalSchedule)
class GoalSchedulAdmin(admin.ModelAdmin):
    form = GoalScheduleChangeForm
    add_form = GoalScheduleCreationForm
    model = GoalSchedule

    inlines = [TextBookingInline]

    fieldsets = (
        ("info", {"fields": ("user_id", "goal_name", "goal_description",)}),
        ("time", {"fields": ("start", "end",)}),
    )
    list_display = ('user_id', 'goal_name', 
        'goal_description', 'start', 'end', )