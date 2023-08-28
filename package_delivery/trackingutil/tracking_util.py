from datetime import datetime


# Function to format float to time in 24-hour format
def float_time_24hr_str(time_float):
    """
    Format the given time in float as a string in 24-hour format (HH:MM).

    Parameters:
        time_float (float): The time to be formatted, represented as a decimal number.

    Returns:
        str: The formatted time string in 24-hour format (HH:MM).
    """
    hours = int(time_float)
    minutes = int((time_float - hours) * 60)
    formatted_time = f"{hours:02d}:{minutes:02d}"
    return formatted_time


def convert_time_str_to_datetime(time_str):
    """
    Convert a time string to a datetime object.

    Args:
        time_str (str): The time string in the format '%H:%M'.

    Returns:
        datetime.time: The converted time as a datetime.time object.
    """
    if time_str is None:
        print(f"Warning: Could not convert time_delivered_str from {time_str} to datetime.time object.")
        return None
    return datetime.strptime(time_str, '%H:%M').time()


# Function to convert 12-hour time to 24-hour time
def convert_12h_to_24h_datetime(time_str):
    """
    Convert a time string from 12-hour format to 24-hour format.

    Parameters:
        time_str (str): The time string to be converted. It should be in the format 'hh:mm AM/PM'.

    Returns:
        datetime.time: The converted time in 24-hour format.
    """
    if time_str == 'EOD':
        return datetime.strptime('5:00 PM', '%I:%M %p').time()
    return datetime.strptime(time_str, '%I:%M %p').time()


# Function to validate time

def validate_time_format(time_str):
    """
    Validate the format of a given time.

    Parameters:
        time_str (str): The time to be validated. Should be in 'HH:MM AM/PM' format.

    Returns:
        bool: True if the time format is valid, False otherwise.
    """
    try:
        datetime.strptime(time_str, '%H:%M %p')
        return True
    except ValueError:
        print("Invalid time format! Please use 'HH:MM AM/PM' format.")
        return False
