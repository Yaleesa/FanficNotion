import requests
import json
import logging

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

headers = {
    "Authorization": "Bearer " + settings['NOTION_API_TOKEN'],
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


class DatabaseEntryUpdate:
    def __init__(self, data, parent_id):
        self.url = "https://api.notion.com/v1/pages/"
        self.data = {"properties": data}
        self.parent_id = {"parent": {"database_id": parent_id}}
        self.icon = {"icon": {"type": "external", "external": {"url": "https://img.icons8.com/ios/250/000000/book.png"}}}

    def build_request(self):
        payload = {**self.parent_id, **self.icon, **self.data}
        response = requests.post(self.url, json=payload, headers=headers)

        return response.json()


class DatabaseUpdate:
    def __init__(self, title, data):
        self.url = f"https://api.notion.com/v1/databases/{settings['DATABASE_ID']}"
        self.data = data
        self.title = [{"text": {"content": title}}]

    def build_request(self):
        payload = {"title": self.title, "properties": self.data}
        response = requests.patch(self.url, json=payload, headers=headers)

        return response.json()


class DatabaseRead:
    def __init__(self, database_id=settings['DATABASE_ID']):
        self.url = f"https://api.notion.com/v1/databases/{database_id}/query"
        self.payload = {"page_size": 100}

    def get_pages(self, num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """

        get_all = num_pages is None
        self.payload['page_size'] = 100 if get_all else num_pages

        # payload = {"page_size": page_size}
        #{"page_size": page_size, "filter": {"property": "Reading Status", "select": {"equals": "Reading"}}}
        results = []
        try:
            response = requests.post(self.url, json=self.payload, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            results.extend(data["results"])

            while data["has_more"] and get_all:
                self.payload['start_cursor'] = data["next_cursor"]
                response = requests.post(self.url, json=self.payload, headers=headers)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                data = response.json()
                results.extend(data["results"])
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            raise Exception("HTTP request failed") from None

        return results
    
    def dump_to_file(self, data):
        with open('db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    db_read = DatabaseRead()
    results = db_read.get_pages()
    # db_read.dump_to_file(results)
    print(results)
    # print(json.dumps(results[0]["properties"]["Pairing"]))
# print(json.dumps(results[1]["properties"]["Fandom"]))
