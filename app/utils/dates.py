from datetime import datetime, timedelta


def date_from_now(days: int) -> datetime:
    """
    Calculates the datetime that is `days` from the current datetime.

    :param days: the number of days to add or subtract from the current datetime
    :type days: int
    :return: the datetime that is `days` from the current date
    :rtype: datetime.datetime
    """
    return datetime.now() + timedelta(days=days)


def days_since(date_in: datetime) -> int:
    """
    :param date_in: The input date as a datetime object to calculate the number of days since.
    :return: The number of days since the input date as an integer.
    """
    return (datetime.now() - date_in.replace(tzinfo=None)).days


def now():
    return datetime.now()


def current_time():
    return datetime.now().time()


def tomorrow():
    return datetime.now() + timedelta(days=1)


def start_today():
    return datetime.now().replace(hour=00, minute=00, second=00)


def end_today():
    return datetime.now().replace(hour=23, minute=59, second=59)


months_en_to_es = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}
