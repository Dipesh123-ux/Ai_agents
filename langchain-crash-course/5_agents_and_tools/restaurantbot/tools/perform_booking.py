import dateparser
from langchain.tools import StructuredTool
from db.models import Booking

def perform_booking(
    customer_name: str,
    customer_email: str,
    date_time_str: str,
    num_people_str: str
):
    """
    Simple booking function for LangChain tool without extensive validations.
    """
    date_time = dateparser.parse(date_time_str, settings={'PREFER_DATES_FROM': 'future'})
    if not date_time:
        return "Error: Unable to parse the date and time. Please provide a valid input."

    try:
        num_people = int(num_people_str)
    except ValueError:
        return "Error: Number of people must be a valid integer."

    if "@" not in customer_email:
        return "Error: Invalid email address."

    try:
        booking = Booking(
            customer_name=customer_name,
            customer_email=customer_email,
            date_time=date_time,
            num_people=num_people
        )
        booking.save()

        return f"Booking confirmed for {customer_name} on {date_time.strftime('%Y-%m-%d %I:%M %p')} for {num_people} people."
    except Exception as e:
        return f"Error saving booking: {e}"

perform_booking_tool = StructuredTool.from_function(
    func=perform_booking,
    name="Perform Booking",
    description=(
        "Use this tool to create a customer booking by providing all required parameters:\n"
        "- customer_name: The full name of the customer (e.g., 'John Doe').\n"
        "- customer_email: A valid email address (e.g., 'john.doe@example.com').\n"
        "- date_time_str: A natural language date/time string (e.g., 'tomorrow 7PM', 'next Friday at 8:30 AM', '9th of December 8PM'). "
        "It should parse into a future date.\n"
        "- num_people_str: The number of guests as a positive integer in string form (e.g., '3').\n\n"
        
        "If any parameter is missing or invalid, the tool will return an error message. "
        "If all parameters are valid, the tool will confirm the booking with the parsed date, time, and the number of guests.\n\n"
        
        "Examples of valid input:\n"
        "{\n"
        "  'customer_name': 'Dipesh',\n"
        "  'customer_email': 'jaswanidipesh8@gmail.com',\n"
        "  'date_time_str': '9th of December 8PM',\n"
        "  'num_people_str': '3'\n"
        "}\n"
        "// This should parse the date '9th of December 8PM' into a future datetime and confirm the booking.\n\n"
        
        "Another valid example:\n"
        "{\n"
        "  'customer_name': 'John Doe',\n"
        "  'customer_email': 'john.doe@example.com',\n"
        "  'date_time_str': 'tomorrow 7PM',\n"
        "  'num_people_str': '2'\n"
        "}\n\n"
        
        "Example of missing parameter:\n"
        "{\n"
        "  'customer_name': 'Alice',\n"
        "  'customer_email': 'alice@example.com',\n"
        "  'num_people_str': '2'\n"
        "}\n"
        "// This will produce an error because 'date_time_str' is missing.\n\n"
        
        "Example of invalid email:\n"
        "{\n"
        "  'customer_name': 'Bob',\n"
        "  'customer_email': 'bobexample.com',\n"
        "  'date_time_str': 'tomorrow at noon',\n"
        "  'num_people_str': '4'\n"
        "}\n"
        "// This will produce an error because the email is not in a valid format.\n\n"
        
        "Always provide all four parameters correctly to ensure a successful booking."
    )
)
