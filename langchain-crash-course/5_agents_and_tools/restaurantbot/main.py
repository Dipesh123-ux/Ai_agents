from utils.db_connection import initialize_db
from db.models import MenuItem
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from tools.get_menu import get_menu_tool
from tools.check_availability import check_availability_tool
from tools.perform_booking import perform_booking_tool
from tools.show_bookings import show_bookings_tool

from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

load_dotenv()

tools = [
    get_menu_tool,
    check_availability_tool,
    perform_booking_tool,
    show_bookings_tool
]

prompt = hub.pull("hwchase17/structured-chat-agent")
llm = ChatOpenAI(model="gpt-4o")

memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True
)

agent = create_structured_chat_agent(llm=llm, tools=tools, prompt=prompt)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,
    max_iterations=3,  
    max_execution_time=30,  
    return_intermediate_steps=False, 
    early_stopping_method="force"
)

def populate_menu():
    if MenuItem.objects.count() == 0:
        items = [
            # Pizzas
            {
                "name": "Margherita Pizza",
                "description": "Classic tomato sauce, mozzarella, and fresh basil.",
                "price": 10
            },
            {
                "name": "Pepperoni Pizza",
                "description": "Tomato sauce, mozzarella, and sliced pepperoni.",
                "price": 12
            },
            {
                "name": "Quattro Formaggi Pizza",
                "description": "Tomato sauce with mozzarella, gorgonzola, parmesan, and fontina.",
                "price": 14
            },
            {
                "name": "Hawaiian Pizza",
                "description": "Tomato sauce, mozzarella, ham, and pineapple.",
                "price": 13
            },

            # Pastas
            {
                "name": "Spaghetti Carbonara",
                "description": "Spaghetti with eggs, pecorino cheese, pancetta, and black pepper.",
                "price": 12
            },
            {
                "name": "Penne Arrabbiata",
                "description": "Penne pasta in a spicy tomato and garlic sauce.",
                "price": 11
            },
            {
                "name": "Fettuccine Alfredo",
                "description": "Fettuccine pasta tossed in a butter, cream, and parmesan sauce.",
                "price": 13
            },
            {
                "name": "Spinach & Ricotta Ravioli",
                "description": "Homemade ravioli filled with spinach and ricotta cheese, served in a light butter sauce.",
                "price": 15
            },

            # Salads
            {
                "name": "Caesar Salad",
                "description": "Romaine lettuce, croutons, and parmesan with Caesar dressing.",
                "price": 8
            },
            {
                "name": "Greek Salad",
                "description": "Tomatoes, cucumbers, onions, olives, and feta cheese with olive oil dressing.",
                "price": 9
            },
            {
                "name": "Caprese Salad",
                "description": "Fresh mozzarella, tomatoes, basil, and balsamic glaze.",
                "price": 10
            },

            # Desserts
            {
                "name": "Tiramisu",
                "description": "Layered espresso-soaked ladyfingers with mascarpone cream and cocoa.",
                "price": 7
            },
            {
                "name": "Panna Cotta",
                "description": "Silky cream dessert topped with a berry coulis.",
                "price": 7
            },
            {
                "name": "Gelato",
                "description": "Homemade Italian ice cream, assorted flavors.",
                "price": 6
            },
        ]
        for item in items:
            menu_item = MenuItem(**item)
            menu_item.save()


def main():
    initialize_db()
    populate_menu()

    admin_restaurant_name = input("Admin: Please enter the restaurant name: ").strip()
    if not admin_restaurant_name:
        admin_restaurant_name = "The Good Restaurant" 

    initial_message = (
        f"You are a helpful virtual assistant for a restaurant called {admin_restaurant_name}. "
        "Your purpose is to assist customers with a variety of requests: "
        "providing the menu, checking table availability, making bookings, and showing their bookings. "
        "Always respond in a polite, friendly, and helpful manner. Give clear, concise, and accurate information. "
        "If a customer needs guidance on placing a booking or understanding the menu, lead them step-by-step. "
        "Your goal is to ensure the customer has a smooth and pleasant experience."
    )

    memory.chat_memory.add_message(SystemMessage(content=initial_message))

    while True:
        # Prompt the user in blue with an emoji
        user_input = input(Fore.BLUE + "👤 User: " + Style.RESET_ALL)
        if user_input.lower() == "exit":
            break

        memory.chat_memory.add_message(HumanMessage(content=user_input))
        
        response = agent_executor.invoke({"input": user_input})
        
        # Print the bot's response in green with an emoji and a decorative line after
        print(Fore.GREEN + "🤖 Bot:" + Style.RESET_ALL, response["output"])
        print(Fore.MAGENTA + "────────────────────────────────────────" + Style.RESET_ALL)

        memory.chat_memory.add_message(AIMessage(content=response["output"]))

if __name__ == "__main__":
    main()
