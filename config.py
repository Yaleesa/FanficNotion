from dotenv import dotenv_values

secrets = dotenv_values(".env")


class Settings:
    NOTION_API_TOKEN = secrets["NOTION_API_TOKEN"]
    DATABASE_ID = secrets["DATABASE_ID"]
    DATABASE_ID_TEST = secrets["DATABASE_ID_TEST"]

    DATABASE_ID = DATABASE_ID_TEST

    #Tijdelijk
    URL = secrets["URL"]


settings = Settings()
