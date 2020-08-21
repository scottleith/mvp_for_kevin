import datetime as dt
import pytz

def convert_to_utc(datetime_obj):
    """
    Convert datetime object to UTC.
    """
    utc_dt = datetime_obj.astimezone( pytz.utc )
    return utc_dt

def change_tz_only(datetime_obj, local_tz):
    """
    Given a datetime and a timezone, safely staple the timezone to the 
    datetime object, regardless of what timezone may already be there.
    """
    assert isinstance(local_tz, str)
    local_tz = pytz.timezone(local_tz)
    local_dt = dt.datetime(
            datetime_obj.year,
            datetime_obj.month,
            datetime_obj.day,
            datetime_obj.hour,
            datetime_obj.minute,
            30
        )
    local_dt = local_tz.localize(local_dt)
    return local_dt
