from datetime import datetime

from dateutil import parser

TIME_MAP = {
    "mon": "monday",
    "tue": "tuesday",
    "wed": "wednesday",
    "thu": "thursday",
    "fri": "friday",
    "sat": "saturday",
    "sun": "sunday",
    "jan": "january",
    "feb": "february",
    "mar": "march",
    "apr": "april",
    "may": "may",
    "jun": "june",
    "jul": "july",
    "aug": "august",
    "sep": "september",
    "sept": "september",
    "oct": "october",
    "nov": "november",
    "dec": "december",
    "mon": "monday",
    "tue": "tuesday",
    "wed": "wednesday",
    "thu": "thursday",
    "thur": "thursday",
    "fri": "friday",
    "sat": "saturday",
    "sun": "sunday",
}
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
MONTHS = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
]


def is_month_or_weekday(s: str):
    if isinstance(s, str):
        if s.lower() in TIME_MAP or (
            s[0:3].lower() in TIME_MAP and s.lower() == TIME_MAP[s[0:3].lower()]
        ):
            return True
    return False


def convert_month_or_weekday_to_int(s: str) -> int:
    if is_month_or_weekday(s):
        if s[0:3].lower() in WEEKDAYS:
            return WEEKDAYS.index(s[0:3].lower()) + 1
        if s[0:3].lower() in MONTHS:
            return MONTHS.index(s[0:3].lower()) + 1
    return -1


def is_datetime(s):
    # consider month and weekday as nominal
    if is_month_or_weekday(s):
        return False
    try:
        parser.parse(s)
        return True
    except ValueError:
        return False


def check_time_format(time_str, time_format):
    try:
        datetime.strptime(time_str, time_format)
        return True
    except ValueError:
        return False


def parse_time_to_timestamp(time_str):
    # 0:00 is prone to bias
    if check_time_format(time_str, "%Y"):
        time_str = time_str + "-01-01 00:00:10"
    elif check_time_format(time_str, "%Y-%m"):
        time_str = time_str + "-01 00:00:10"
    elif check_time_format(time_str, "%Y-%m-%d"):
        time_str = time_str + " 00:00:10"

    try:
        parsed_time = parser.parse(time_str)
        timestamp = parsed_time.timestamp()
        return timestamp
    except Exception:
        return None


def parse_timestamp_to_time(timestamp):
    # todo: extract date format
    date_format = "%Y-%m-%d"
    try:
        parsed_time = datetime.fromtimestamp(timestamp)
        time_str = parsed_time.strftime(date_format)
        return time_str
    except Exception:
        return None


# handle case like 2008.436089
def parse_number_to_time(number):
    if number > 0 and number < 2999:
        timestamp = parse_time_to_timestamp(str(int(number)))
        timestamp += (number - int(number)) * 365 * 24 * 60 * 60
        return timestamp
    return number


def compare_time_strings(time_str1: str, time_str2: str):
    try:
        if parser.parse(time_str1).timestamp() == parser.parse(time_str2).timestamp():
            return True
    except Exception:
        pass

    try:
        str1 = TIME_MAP.get(time_str1.lower(), time_str1)
        str2 = TIME_MAP.get(time_str2.lower(), time_str2)

        if str1.lower() == str2.lower():
            return True

        if (
            is_month_or_weekday(str1)
            and str(convert_month_or_weekday_to_int(str1)) == str2
        ):
            return True
        if (
            is_month_or_weekday(str2)
            and str(convert_month_or_weekday_to_int(str2)) == str1
        ):
            return True

        if (
            is_month_or_weekday(str1)
            and str(convert_month_or_weekday_to_int(str1)) == str2
        ):
            return True
        if (
            is_month_or_weekday(str2)
            and str(convert_month_or_weekday_to_int(str2)) == str1
        ):
            return True

        if is_month_or_weekday(str2) and parse_time_to_timestamp(time_str1) is not None:
            # weekday
            if (
                str2.lower()
                == datetime.fromtimestamp(parse_time_to_timestamp(time_str1))
                .strftime("%A")
                .lower()
            ):
                return True
            # month
            if (
                str2.lower()
                == datetime.fromtimestamp(parse_time_to_timestamp(time_str1))
                .strftime("%B")
                .lower()
            ):
                return True
        if is_month_or_weekday(str1) and parse_time_to_timestamp(time_str2) is not None:
            # weekday
            if (
                str1.lower()
                == datetime.fromtimestamp(parse_time_to_timestamp(time_str2))
                .strftime("%A")
                .lower()
            ):
                return True
            # month
            if (
                str1.lower()
                == datetime.fromtimestamp(parse_time_to_timestamp(time_str2))
                .strftime("%B")
                .lower()
            ):
                return True

        return False
    except Exception:
        return False
