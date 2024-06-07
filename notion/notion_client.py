import requests
import json

from config import settings

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
    def get_fics(database_id=settings['DATABASE_ID'], num_pages=None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{database_id}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        #{"page_size": page_size, "filter": {"property": "Reading Status", "select": {"equals": "Reading"}}}
        response = requests.post(url, json=payload, headers=headers)

        data = response.json()
        print(data)
        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{settings['DATABASE_ID']}/query"
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            results.extend(data["results"])

        return results
    
    def dump_to_file(data):
        with open('db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# print(json.dumps(results[1]["properties"]["Fandom"]))
