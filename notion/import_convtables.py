from .notion_client import DatabaseRead


class ConversionTables:
    def __init__(self):
        self.ship_table: dict = self.importShiptables()
        self.fandom_table: dict = self.importFandomTable()

    def importShiptables(self, database_id='39a4ea42248b4abb8df3c060597a5edf'):
        response = DatabaseRead(database_id=database_id).get_pages()
        return {row['properties']['Full Notation']['title'][0]['plain_text']: row['properties']['Ship Name']['rich_text'][0]['plain_text'] for row in response}

    def importFandomTable(self, database_id='d893f39a4fea4867abdd7700d377be00'):
        response = DatabaseRead(database_id=database_id).get_pages()
        return {row['properties']['Name on Site']['title'][0]['plain_text']: row['properties']['Name FFDB']['rich_text'][0]['plain_text'] for row in response}


class CheckDoubleEntry:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def check(self, database_id='c1e2eeb6100e4a95a3803c646c6963fd'):
        response = DatabaseRead(database_id=database_id).get_pages()
        for row in response:
            if row['properties']['Fanfiction Title']['title'][0]['plain_text'] == self.title and row['properties']['Author']['rich_text'][0]['text']['content'].strip() == self.author[0]['name']:
                return True
