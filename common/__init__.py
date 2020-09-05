import datetime


def time_as_dict(time: datetime):
    minutes = time.seconds // 60
    hours = minutes // 60
    weeks = time.days // 7
    time_dict = {
        'days': time.days % 7,
        'minutes': minutes % 60,
        'hours': hours % 24,
        'weeks': weeks,
        'years': time.days // 365
    }
    return time_dict