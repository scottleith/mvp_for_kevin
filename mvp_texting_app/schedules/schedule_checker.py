import django

django.setup() 

import twilio
import environ

from django.utils import timezone
from django.contrib.auth import get_user_model

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime as dt, timedelta
from config.twilio import client

from mvp_texting_app.schedules.models import TextBooking
from mvp_texting_app.persons.models import PersonPhone

User = get_user_model()
sched = BlockingScheduler(timezone = 'UTC')

env = environ.Env()
twilio_num = env('TWILIO_NUM_0')

SCHEDULE_CHECKER_WINDOW_MINS = 2

def get_texts_next_N_mins(mins = SCHEDULE_CHECKER_WINDOW_MINS):
    """
    Pulls any and all texts that are scheduled for delivery 
    in the next 2 minutes.
    """
    now = dt.now(timezone.utc)
    bookings = TextBooking.objects.filter(
        final_send_dt__gte = now,
        final_send_dt__lte = now + timedelta(minutes = mins) 
        )
    return bookings
    
def get_text_params(booking):
    """
    Given a booking, return the text content and destination number.
    """
    pid = User.objects.get(username = booking.user_id).person_id
    phone = PersonPhone.objects.get(person_id = pid).phone_number
    phone = "+" + str(phone.country_code) + str(phone.national_number)
    #phone = UserDetails.objects.get(pk = user.id).phone_number
    body = booking.text_id.body
    return phone, str(body)
   
def send_text(from_, to, body):
    try:
        client.messages.create(
            from_ = from_,
            to = to,
            body = body
        )
        print("Message sent successfully")
    except twilio.base.exceptions.TwilioRestException:
        print("Twilio Rest Exception")

@sched.scheduled_job('interval', minutes = SCHEDULE_CHECKER_WINDOW_MINS)
def check_for_texts_and_send():
    """
    Job that runs every X minutes.
    Looks for texts to send in the next X minutes and sends them.
    """
    print("Trying to check for upcoming bookings...")
    bookings = get_texts_next_N_mins()
    print( "Check complete. %s bookings found" % len(bookings) )
    if bookings:
        print("Bookings found! Sending texts...")
        for booking in bookings:
            to_number, body = get_text_params(booking)
            send_text(
                from_ = twilio_num,
                to = to_number,
                body = body
                )
    else:
        print("No bookings this round. Let's try again in 2 minutes.")

sched.start()
