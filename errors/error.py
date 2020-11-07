class DateTimeError(Exception):
    pass

class DateError(DateTimeError):
    pass

class TimeError(DateTimeError):
    pass