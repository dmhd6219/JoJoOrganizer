class DateTimeError(Exception):
    pass


class DateError(DateTimeError):
    pass


class TimeError(DateTimeError):
    pass


class TitleError(Exception):
    pass


class EmptyTitle(TitleError):
    pass
