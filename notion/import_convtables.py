from .notion_client import DatabaseRead


class ConversionTables:
    def __init__(self):
        self.ship_table: dict = self.importShiptables()
        self.fandom_table: dict = self.importFandomTable()

    def importShiptables(self, database_id='39a4ea42248b4abb8df3c060597a5edf'):
        response = DatabaseRead.get_fics(database_id=database_id)
        return {row['properties']['Full Notation']['title'][0]['plain_text']: row['properties']['Ship Name']['rich_text'][0]['plain_text'] for row in response}

    def importFandomTable(self, database_id='d893f39a4fea4867abdd7700d377be00'):
        response = DatabaseRead.get_fics(database_id=database_id)
        return {row['properties']['Name on Site']['title'][0]['plain_text']: row['properties']['Name FFDB']['rich_text'][0]['plain_text'] for row in response}

