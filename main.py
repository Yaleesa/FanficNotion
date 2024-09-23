import logging
import argparse
from notion.notion_client import DatabaseEntryUpdate
from notion.notionficdb import FanficDatabaseEndpoint
from content_scraper.ao3_scraping import AO3Fic, get_page
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_content(url):
    # scrape page
    if url.startswith("https://archiveofourown.org"):
        try:
            return AO3Fic(get_page(url))
        except Exception as e:
            logger.error(e)
            raise
    else:
        raise ValueError("URL is not from AO3")


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
    logger.info(payload_data) 
    return payload_data


def send_to_notion(data):
    return DatabaseEntryUpdate(parent_id=settings['DATABASE_ID'], data=data).build_request()


def run(url):
    scraped_fic = scrape_content(url)
    data = build_data(scraped_fic)
    return send_to_notion(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape fanfic data and send to Notion.")
    parser.add_argument('--url', type=str, help='URL of the fanfic to scrape')
    args = parser.parse_args()

    if args.url:
        logger.info(f"Scraping {args.url}")  
        try:
            run(args.url)
        except ValueError as e:
            logger.error(e)
            raise
    else:
        logger.warning("No URL provided, using default url")
        logger.info(f"Scraping {settings['URL']}")  
        try:
            run(settings['URL'])
        except ValueError as e:
            logger.error(e)
            raise
