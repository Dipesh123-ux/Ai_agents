from mongoengine import connect

db_password = "dipesh12"
connection_string = f"mongodb+srv://jaswanidipesh8:{db_password}@cluster0.ueqmu.mongodb.net/"

def initialize_db():
    connect(
        db="restaurantAgent",
        host=connection_string,
        alias="default"
    )
    print("connected to mongodb database")
