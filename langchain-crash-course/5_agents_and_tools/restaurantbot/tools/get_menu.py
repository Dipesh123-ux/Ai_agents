from langchain.tools import  StructuredTool
from db.models import MenuItem

def get_menu():
    """
    Returns the menu items of the restaurant.
    """
    menu_items = MenuItem.objects()
    menu_str = "\n".join([
        f"{item.name}: {item.description} - ${item.price}"
        for item in menu_items
    ])
    return menu_str if menu_str else "The menu is currently empty."

get_menu_tool =  StructuredTool.from_function(
    func=get_menu,
    name="Get Menu",
    description="Use this to get the menu of the restaurant."
)
