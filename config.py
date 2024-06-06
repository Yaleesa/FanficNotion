from dotenv import dotenv_values
import os

secrets = dotenv_values(".env")

settings = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
# class Settings:
    
#     # NOTION_API_TOKEN = secrets["NOTION_API_TOKEN"]
#     # DATABASE_ID = secrets["DATABASE_ID"]
#     # DATABASE_ID_TEST = secrets["DATABASE_ID_TEST"]

#     # DATABASE_ID = DATABASE_ID_TEST

#     # #Tijdelijk
#     # URL = secrets["URL"]


# settings = Settings()
