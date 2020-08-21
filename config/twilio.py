import environ

from twilio.rest import Client

env = environ.Env()

client = Client(env('TWILIO_SID'), env('TWILIO_AUTH_TOKEN'))
