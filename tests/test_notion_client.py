import unittest
from unittest.mock import patch, Mock
import json
import os
from notion.notion_client import DatabaseRead, DatabaseEntryUpdate, headers


class TestDatabaseRead(unittest.TestCase):

    @patch('notion.notion_client.requests.post')
    def test_get_pages_all_pages(self, mock_post):
        # Mock response for the first call
        mock_response_1 = Mock()
        mock_response_1.json.return_value = {
            "results": [{"id": "page1"}],
            "has_more": True,
            "next_cursor": "cursor1"
        }
        
        # Mock response for the second call
        mock_response_2 = Mock()
        mock_response_2.json.return_value = {
            "results": [{"id": "page2"}],
            "has_more": False
        }
        
        # Set the side effect of the mock to return the two responses
        mock_post.side_effect = [mock_response_1, mock_response_2]
        
        db_read = DatabaseRead()
        results = db_read.get_pages()

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "page1")
        self.assertEqual(results[1]["id"], "page2")

    @patch('notion.notion_client.requests.post')
    def test_get_pages_limited_pages(self, mock_post):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{"id": "page1"}, {"id": "page2"}],
            "has_more": False
        }
        
        mock_post.return_value = mock_response
        
        db_read = DatabaseRead()
        results = db_read.get_pages(num_pages=2)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["id"], "page1")
        self.assertEqual(results[1]["id"], "page2")

    def test_dump_to_file(self):
        data = {"key": "value"}
        DatabaseRead.dump_to_file(data)
        
        with open('db.json', 'r', encoding='utf8') as f:
            file_data = json.load(f)
        
        self.assertEqual(file_data, data)
        
        # Clean up
        os.remove('db.json')


class TestDatabaseEntryUpdate(unittest.TestCase):

    @patch('notion.notion_client.requests.post')
    def test_build_request_success(self, mock_post):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"id": "new_page_id"}
        mock_post.return_value = mock_response

        data = {"Name": {"title": [{"text": {"content": "Test Page"}}]}}
        parent_id = "test_parent_id"
        db_entry_update = DatabaseEntryUpdate(data, parent_id)

        response = db_entry_update.build_request()

        self.assertEqual(response["id"], "new_page_id")
        mock_post.assert_called_once_with(
            "https://api.notion.com/v1/pages/",
            json={
                "parent": {"database_id": parent_id},
                "icon": {"type": "external", "external": {"url": "https://img.icons8.com/ios/250/000000/book.png"}},
                "properties": data
            },
            headers=headers
        )

    @patch('notion.notion_client.requests.post')
    def test_build_request_failure(self, mock_post):
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"object": "error", "status": 400, "message": "Invalid request"}
        mock_post.return_value = mock_response

        data = {"Name": {"title": [{"text": {"content": "Test Page"}}]}}
        parent_id = "test_parent_id"
        db_entry_update = DatabaseEntryUpdate(data, parent_id)

        response = db_entry_update.build_request()

        self.assertEqual(response["object"], "error")
        self.assertEqual(response["status"], 400)
        self.assertEqual(response["message"], "Invalid request")
        mock_post.assert_called_once_with(
            "https://api.notion.com/v1/pages/",
            json={
                "parent": {"database_id": parent_id},
                "icon": {"type": "external", "external": {"url": "https://img.icons8.com/ios/250/000000/book.png"}},
                "properties": data
            },
            headers=headers
        )


if __name__ == '__main__':
    unittest.main()
