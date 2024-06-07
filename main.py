from notion.notion_client import DatabaseEntryUpdate
from notion.notionficdb import FanficDatabaseEndpoint
from content_scraper.ao3_scraping import AO3Fic, get_page
from config import settings

print(f"url from settings: {settings['URL']}")


def scrape_content(url=settings['URL']):
    # scrape page
    return AO3Fic(get_page(url))


def build_data(scraped_fic):
    # convert to database/page endpoint
    payload_data = FanficDatabaseEndpoint(
        fanfic_title=scraped_fic.title, 
        fandom=scraped_fic.fandom,
        authors=scraped_fic.authors,
        word_count=int(scraped_fic.word_count.replace(",", "")),
        fic_link=settings['URL'],
        summary=scraped_fic.summary,
        pairings=scraped_fic.relationships,
        reading_status="Not Read",
        series=scraped_fic.series,
        chapters=int(scraped_fic.chapters.split("/")[0]),
        fic_rating=scraped_fic.rating,
        fic_status=scraped_fic.status,
        fic_site=scraped_fic.fanfic_site,
        published=scraped_fic.published,
        last_updated=scraped_fic.last_updated
        )
    # vieze hack om alle parent values weg te halen 
    payload_data = dict(prop for val in vars(payload_data).values() for prop in val.items())
    print(payload_data)  # logger
    return payload_data


def send_to_notion(data):
    return DatabaseEntryUpdate(parent_id=settings['DATABASE_ID'], data=data).build_request()


def go():
    return send_to_notion(build_data(scraped_fic=scrape_content()))



