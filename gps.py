import datetime

def utc_to_weekseconds(utc_timestamp, leapseconds):
    """ Returns the GPS week, the GPS day, and the seconds
        and microseconds since the beginning of the GPS week
        https://stackoverflow.com/questions/45422739/gps-time-in-weeks-since-epoch-in-python
    """
    import datetime
    import calendar
    utc = datetime.datetime.fromtimestamp(utc_timestamp)
    datetimeformat = "%Y-%m-%d %H:%M:%S"
    epoch = datetime.datetime.strptime("1980-01-06 00:00:00", datetimeformat)
    tdiff = utc - epoch + datetime.timedelta(seconds=leapseconds)
    gpsweek = tdiff.days // 7
    gpsdays = tdiff.days - 7*gpsweek
    gpsseconds = tdiff.seconds + 86400 * (tdiff.days - 7*gpsweek)
    return gpsweek, gpsdays, gpsseconds, tdiff.microseconds, gpsseconds+(tdiff.microseconds / 10**6)




def gps_week_second_to_unix_time(gps_week, start_second, end_second):
    # GPS epoch (January 6, 1980) in UTC
    gps_epoch_utc = datetime.datetime(1980, 1, 6, 0, 0, 0)

    # Number of seconds in a GPS week
    seconds_per_week = 604800

    # Compute the total number of seconds from GPS epoch to the start and end seconds
    start_total_seconds = gps_week * seconds_per_week + start_second
    end_total_seconds = gps_week * seconds_per_week + end_second

    # Compute the UNIX time for start and end seconds by adding the total seconds to the GPS epoch in UTC
    start_unix_time = (gps_epoch_utc + datetime.timedelta(seconds=start_total_seconds)).timestamp()
    end_unix_time = (gps_epoch_utc + datetime.timedelta(seconds=end_total_seconds)).timestamp()

    return int(start_unix_time), int(end_unix_time)