from django.contrib import admin
from django.contrib.auth import get_user_model

from mvp_texting_app.programs.models import (
    TextingProgram, 
    TextingProgramSchedule, 
    TextingProgramParticipantRecord,
)


class TextingProgramScheduleInline(admin.StackedInline):
    """
    Add the texts when you create a program.
    """
    model = TextingProgramSchedule
    extra = 0

class TextingProgramParticipantRecordInline(admin.StackedInline):
    """
    Add a participant record when you add a program.
    """
    model = TextingProgramParticipantRecord
    extra = 0


@admin.register(TextingProgram)
class TextingProgramAdmin(admin.ModelAdmin):
    model = TextingProgram

    inlines = [
        TextingProgramScheduleInline,
        TextingProgramParticipantRecordInline,
        ]

    fieldsets = (
            ("info", 
            {"fields": ("name", "n_texts", "runtime_days",)}
            ),
        ) 
    list_display = ("id", "name", "n_texts", "runtime_days",)
    search_fields = ("id", "name", "n_texts", "runtime_days",)
    ordering = ('id',)


@admin.register(TextingProgramSchedule)
class TextingProgramScheduleAdmin(admin.ModelAdmin):
    model = TextingProgramSchedule

    fieldsets = (
            ("info", 
            {"fields": ("program_id", "text_id", "position", "delta_days",)}
            ),
        ) 
    list_display = ("program_id", "text_id", "position", "delta_days",)
    search_fields = ("program_id", "text_id", "position", "delta_days",)
    ordering = ('program_id', 'position',)


@admin.register(TextingProgramParticipantRecord)
class TextingProgramParticipantRecordAdmin(admin.ModelAdmin):
    model = TextingProgramParticipantRecord

    fieldsets = (
            ("info", 
            {"fields": ("user_id", "program_id", "start", "end", "active",
                "abandoned",)}
            ),
        ) 
    list_display = ("user_id", "program_id", "start", "end", "active",
                "abandoned",)
    search_fields = (("user_id", "program_id", "start", "end", "active",
                "abandoned",)
    ordering = ('program_id', 'user_id', )
