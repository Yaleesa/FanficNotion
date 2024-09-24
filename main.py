import logging
import argparse
import json
from notion.notion_client import DatabaseEntryUpdate, DatabaseRead
from notion.notionficdb import FanficDatabaseEndpoint
from notion.import_convtables import CheckDoubleEntry
from content_scraper.ao3_scraping import AO3Fic, get_page
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def global_exception_handler(exc_type, exc_value, exc_traceback):
#     if issubclass(exc_type, KeyboardInterrupt):
#         sys.__excepthook__(exc_type, exc_value, exc_traceback)
#         return
#     logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# # Set the global exception handler
# sys.excepthook = global_exception_handler


def scrape_content(url):
    # scrape page
    if url.startswith("https://archiveofourown.org"):
        if 'chapter' in url:
            url = url.split("/chapter")[0]
        return AO3Fic(get_page(url))
    else:
        raise ValueError("URL is not from AO3")


def build_data(scraped_fic, url):
    # convert to database/page endpoint
    payload_data = FanficDatabaseEndpoint(
        fanfic_title=scraped_fic.title, 
        fandom=scraped_fic.fandom,
        authors=scraped_fic.authors,
        word_count=int(scraped_fic.word_count.replace(",", "")),
        fic_link=url,
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


def send_fic_to_notion(url, check_double=True):
    scraped_fic = scrape_content(url)

    if check_double and CheckDoubleEntry(scraped_fic.title, scraped_fic.authors).check():
        logger.warning("Fic already in database, not sending to Notion")
        return

    data = build_data(scraped_fic, url)
    return send_to_notion(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape fanfic data and send to Notion.")
    parser.add_argument('--url', type=str, help='URL of the fanfic to scrape')
    parser.add_argument('--test', action='store_true', help='Run tests')
    parser.add_argument('--log', type=str, help='Log level', default='INFO')
    parser.add_argument('--function', type=str, help='function to use', default='send_fic_to_notion')

    args = parser.parse_args()

    if args.function == 'send_fic_to_notion':
        if not args.url:
            logger.warning("No URL provided, using default url")
        url = args.url if args.url else settings['URL']
        logger.info(f"Scraping {url}")  
        try:
            send_fic_to_notion(url, check_double=True)
        except ValueError as e:
            logger.error(e)
            raise
    elif args.function == 'read_database':
        results = DatabaseRead().get_pages()
        print(len(results))
        print(json.dumps(results[0]["properties"]["Pairing"]))
        print(
            [
                (
                    result["properties"]["Fanfiction Title"]["title"][0]["text"]["content"],
                    result["properties"]["Author"]["rich_text"][0]["text"]["content"].strip(),
                )
                for result in results
            ]
        )
