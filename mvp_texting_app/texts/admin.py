from django.contrib import admin
from django.contrib.auth import get_user_model

from mvp_texting_app.schedules.models import TextBooking
from mvp_texting_app.texts.forms import (
    TextDetailsChangeForm, TextDetailsCreationForm
)
from mvp_texting_app.texts.models import TextDetails


class TextBookingInline(admin.StackedInline):
    """
    Create a text booking when you create a text.
    """
    model = TextBooking
    extra = 0


@admin.register(TextDetails)
class TextDetailsAdmin(admin.ModelAdmin):
    form = TextDetailsChangeForm
    add_form = TextDetailsCreationForm
    model = TextDetails

    inlines = [TextBookingInline]

    fieldsets = (
        ("type", {"fields": ("text_type", )}),
        ("body", {'fields': ("body",)}),
        ) 
    list_display = ("id", "text_type", "body","n_chars","created")
    search_fields = ("id", "text_type","created",)
    ordering = ('created',)

