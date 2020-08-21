import datetime as dt

def add_time_to_date( dt_date, dt_time ):
    """
    Take a date and a time and get a datetime!This is here when we want to strip
    out or otherwise be careful about timezone.
    """
    yr = dt_date.year
    mo = dt_date.month
    day = dt_date.day
    hr = dt_time.hour
    minute = dt_time.minute
    return dt.datetime(yr, mo, day, hr, minute)