from .import_convtables import ConversionTables


class FanficDatabaseEndpoint:
    conversionTables = ConversionTables()

    def __init__(self, fanfic_title, fandom, authors, word_count, fic_link, summary, pairings, reading_status, series, chapters, fic_rating, fic_status, fic_site, published, last_updated):
        self.FanficTitle: str = self.FanficTitle(fanfic_title)
        self.Fandom: str = self.Fandom(fandom)
        self.Author: str = self.Author(authors)
        self.Hearts: str
        self.ReadingStatus: str = self.ReadingStatus(reading_status)
        self.Series: str = self.Series(series)
        self.ePub: str
        self.Chapters: int = self.Chapters(chapters)
        self.WordCount: int = self.WordCount(word_count)
        self.Pairing: str = self.Pairing(pairings)
        self.Tropes: str
        self.EraSetting: str
        self.Warnings: str
        self.Summary: str = self.Summary(summary)
        self.FicRating: str = self.FicRating(fic_rating)
        self.FicStatus: str = self.FicStatus(fic_status)
        self.FicSite: str = self.FanficSite(fic_site)
        self.FicLink: str = self.FicLink(fic_link)
        self.Bookmarked: str 
        self.Published: str = self.Published(published)
        self.LastUpdated: str = self.LastUpdated(last_updated)

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

    def Fandom(self, fandoms):
        fandom_table = self.conversionTables.fandom_table
        return {"Fandom": {"id": "%3FuQU", "type": "multi_select", "multi_select": [{"name": fandom_table.get(fandom, fandom)} for fandom in fandoms]}}

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
        ship_table = self.conversionTables.ship_table
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

    def ReadingStatus(self, reading_status):
        return {
            "Reading Status": {
                "id": "UYbn",
                "type": "select",
                "select": {
                    "name": reading_status,
                }
            }
        }

    def FanficSite(self, fanfic_site):
        return {
            "Fanfiction Site": {
                "id": "xSFD",
                "type": "select",
                "select": {"name": fanfic_site}
                }
        }

    def Series(self, series):
        series = series if series else 'Standalone'
        return {
            "Series": {
                    "id": "LqEg",
                    "type": "rich_text",
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": series, "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": series,
                            "href": None
                        }
                    ]
            }
        }
    
    def Chapters(self, chapters):
        return {"Chapters": {"id": "aw%7DN", "type": "number", "number": chapters}}

    def FicRating(self, fic_rating):
        rating_conv = {
            "Explicit": "Explicit / E / MA",
            "Mature": "Mature / M / R",
            "Teen And Up Audiences": "Teen & Up / Over 13 / T",
            "General Audiences": "General / G"
        }
        return {
                "Fanfiction Rating": {
                    "id": "%3DrZO",
                    "type": "select",
                    "select": {"name": rating_conv.get(fic_rating, fic_rating)}
                }
            }

    def FicStatus(self, status):
        status = status if status != "Updated" else "WIP"
        return {
                "Fanfiction Status": {
                    "id": "g%5Dna",
                    "type": "select",
                    "select": {"name": status}
                }
            }
    
    def Published(self, published):
        return {
            "Published": {
                "id": "l%7Duw",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": published, "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": published,
                        "href": None
                    }
                ]
            }
        }

    def LastUpdated(self, last_updated):
        return {
            "Last Updated": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": last_updated, "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        },
                        "plain_text": last_updated,
                        "href": None
                    }
                ]
            }
        }



