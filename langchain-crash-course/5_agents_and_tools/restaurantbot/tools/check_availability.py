import dateparser
from langchain.tools import StructuredTool
from db.models import Booking
from datetime import timedelta

def check_availability(
    date_time_str: str,
    num_people_str: str
):
    """
    Use this tool to check availability for a given date and time, and number of guests.
    
    Parameters:
    - date_time_str: A natural language date/time string (e.g., "tomorrow 7PM", "next Friday at 8:30 AM", "9th of December 8PM").
      It should parse into a future date/time.
    - num_people_str: The number of guests as a positive integer in string form (e.g., "3").

    The tool attempts to parse the provided `date_time_str` using natural language processing. 
    If it fails to parse into a future date/time, it returns an error message. 
    Similarly, if the `num_people_str` cannot be converted to a positive integer, 
    it returns an error message.

    If both parameters are valid, the tool checks the availability within the specified hour. 
    It assumes a maximum capacity of 50 people per hour. It sums up the number of guests 
    from existing bookings within the same 1-hour slot of the provided date/time and 
    determines if the requested number of guests can be accommodated.

    Returns:
    - "Available" if the venue can accommodate the given number of guests.
    - "Not available" if the venue cannot accommodate them.

    Examples of valid input:
    {
      "date_time_str": "9th of December 8PM",
      "num_people_str": "3"
    }

    Another valid example:
    {
      "date_time_str": "tomorrow 7PM",
      "num_people_str": "2"
    }

    Example of invalid date:
    {
      "date_time_str": "yesterday 7PM",
      "num_people_str": "2"
    }
    // This may return an error because the parsed date/time might not be in the future.

    Example of invalid number of people:
    {
      "date_time_str": "tomorrow 7PM",
      "num_people_str": "abc"
    }
    // This will return an error message because 'abc' cannot be converted to an integer.
    """

    date_time = dateparser.parse(date_time_str, settings={'PREFER_DATES_FROM': 'future'})
    if not date_time:
        return "Error: Unable to parse the date and time. Please provide a valid future date/time."

    try:
        num_people = int(num_people_str)
        if num_people <= 0:
            return "Error: Number of people must be a positive integer."
    except ValueError:
        return "Error: Number of people must be a valid integer."

    max_capacity = 50
    start_time = date_time.replace(minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=1)

    try:
        bookings = Booking.objects(
            date_time__gte=start_time,
            date_time__lt=end_time
        )
        total_people = sum(booking.num_people for booking in bookings)
        available = (max_capacity - total_people) >= num_people
        return "Available" if available else "Not available"
    except Exception as e:
        return f"Error checking availability: {e}"


check_availability_tool = StructuredTool.from_function(
    func=check_availability,
    name="Check Availability",
    description=(
        "Use this tool to check if a table is available for a given date/time and number of guests:\n"
        "- date_time_str: A natural language date/time string (e.g., 'tomorrow 7PM', '9th of December 8PM') that should parse into a future date/time.\n"
        "- num_people_str: A positive integer in string form representing the number of guests (e.g., '4').\n\n"
        
        "If the date/time cannot be parsed into a future date, or if the number of people is not a valid positive integer, "
        "the tool returns an error.\n\n"
        
        "If the parameters are valid, it checks if the requested number of guests can be accommodated, assuming a maximum capacity of 50 guests per hour. "
        "It returns 'Available' if there is enough capacity, or 'Not available' otherwise.\n\n"
        
        "Examples:\n"
        "{\n"
        "  'date_time_str': '9th of December 8PM',\n"
        "  'num_people_str': '3'\n"
        "}\n\n"
        
        "{\n"
        "  'date_time_str': 'tomorrow 7PM',\n"
        "  'num_people_str': '2'\n"
        "}\n\n"
        
        "Invalid date/time:\n"
        "{\n"
        "  'date_time_str': 'yesterday 7PM',\n"
        "  'num_people_str': '2'\n"
        "}\n"
        
        "Invalid number of people:\n"
        "{\n"
        "  'date_time_str': 'tomorrow 7PM',\n"
        "  'num_people_str': 'abc'\n"
        "}\n"
    )
)
