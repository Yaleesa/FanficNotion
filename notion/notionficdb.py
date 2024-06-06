class FanficDatabaseEndpoint:
    def __init__(self, fanfic_title, fandom, authors, word_count, fic_link, summary, pairings):
        self.FanficTitle: str = self.FanficTitle(fanfic_title)
        self.Fandom: str = self.Fandom(fandom)
        self.Author: str = self.Author(authors)
        self.Hearts: str
        self.ReadingStatus: str
        self.Series: str
        self.ePub: str
        self.Chapters: str
        self.WordCount: int = self.WordCount(word_count)
        self.Pairing: str = self.Pairing(pairings)
        self.Tropes: str
        self.EraSetting: str
        self.Warnings: str
        self.Summary: str = self.Summary(summary)
        self.FicRating: str
        self.FicStatus: str
        self.FicSite: str
        self.FicLink: str = self.FicLink(fic_link)
        self.Bookmarked: str
        self.Published: str

    def FanficTitle(self, fanfic_title):
        return {
            "Fanfiction Title": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": fanfic_title, "link": None},
                        "annotations": {
                            "bold": True,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": fanfic_title,
                        "href": None,
                    }
                ],
            }
        }

    def Fandom(self, fandom):
        return {"Fandom": {"id": "%3FuQU", "type": "multi_select", "multi_select": [{"name": fandom}]}}

    def Author(self, authors):
        return {
            "Author": {
                "id": "%5BAZr",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"{author['name']} ",
                            "link": {"url": f"https://archiveofourown.org{author['url']}"},
                        },
                        "annotations": {
                            "bold": True,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": author['name'],
                        "href": f"https://archiveofourown.org{author['url']}",
                    }
                    for author in authors
                ],
            }
        }

    def WordCount(self, word_count):
        return {"Word Count": {"id": "Lt%5BK", "type": "number", "number": word_count}}

    def FicLink(self, fic_link):
        return {"Fanfiction Link": {"id": "cUez", "type": "url", "url": fic_link}}

    def Summary(self, summary):
        return {
            "Summary": {
                "id": "%40CFj",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": summary, "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": summary,
                        "href": None,
                    }
                ],
            }
        }

    def Pairing(self, pairings):
        ship_table = {
        }
        return {
            "Pairing": {
                "id": "B%7B%40j",
                "type": "multi_select",
                "multi_select": [
                    {
                        "name": ship_table.get(pairing, pairing),
                    }
                    for pairing in pairings
                    if "/" in pairing
                ],
            }
        }

    # Hearts:
    # ReadingStatus:
    # Series:
    # ePub:
    # Chapters:

    # Pairing:
    # Tropes:
    # EraSetting:
    # Warnings:
    # Summary:
    # FicRating:
    # FicStatus:
    # FicSite:
    # FicLink:
    # Bookmarked:
    # Published:



