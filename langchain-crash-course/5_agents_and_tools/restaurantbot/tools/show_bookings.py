from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from db.models import Booking

class ShowBookingsInput(BaseModel):
    customer_email: str = Field(..., description="Customer's email Id")

def show_bookings(customer_email: str):
    """
    Shows bookings for the customer.
    """
    try:
        
        # Query bookings
        bookings = Booking.objects(customer_email=customer_email)
        if bookings:
            bookings_str = "\n".join([
                f"{b.date_time.strftime('%Y-%m-%d %H:%M')}: {b.num_people} people"
                for b in bookings
            ])
            return bookings_str
        else:
            return "No bookings found for this customer."
    except Exception as e:
        return f"Error fetching bookings: {e}"

show_bookings_tool = StructuredTool.from_function(
    func=show_bookings,
    name="Show Bookings",
    description="Use this to fetch the bookings for a customer on the basis of their emailId."
)
