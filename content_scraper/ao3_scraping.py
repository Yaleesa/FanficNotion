from bs4 import BeautifulSoup 
from lxml import etree 
import requests 


HEADERS = ({'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
            'Accept-Language': 'en-US, en;q=0.5'}) 


def get_page(url):
    webpage = requests.get(url, headers=HEADERS) 
    soup = BeautifulSoup(webpage.content, "html.parser") 
    dom = etree.HTML(str(soup))
    return dom


def get_xpath(dom, path):
    return dom.xpath(path)


class AO3Fic:
    def __init__(self, dom):
        self.dom = dom
        self.fanfic_site = "AO3"
        self.title = get_xpath(self.dom, '//*[@class="title heading"]')[0].text.strip()
        self.fandom = get_xpath(self.dom, '//dd[@class="fandom tags"]//a')[0].text
        self.authors = [{"name": aut.text, "url": aut.attrib['href']} for aut in get_xpath(self.dom, '//*[@rel="author"]')]
        self.word_count = get_xpath(self.dom, '//dl[@class="stats"]/dd[@class="words"]')[0].text
        self.chapters = get_xpath(self.dom, '//dl[@class="stats"]/dd[@class="chapters"]')[0].text
        self.status = get_xpath(self.dom, '//dl[@class="stats"]/dt[@class="status"]')[0].text.strip(":")
        self.published = get_xpath(self.dom, '//dl[@class="stats"]/dd[@class="published"]')[0].text
        self.rating = get_xpath(self.dom, '//dd[@class="rating tags"]//a')[0].text
        self.category = [cat.text for cat in get_xpath(self.dom, '//dd[@class="category tags"]/ul/li/a')]
        self.summary = " ".join([par.text for par in get_xpath(self.dom, '//div[@class="summary module"]//blockquote//p')])
        self.relationships = [cat.text for cat in get_xpath(self.dom, '//dd[@class="relationship tags"]/ul/li/a')]
        self.series = get_xpath(self.dom, '//dd[@class="series"]//span[@class="position"]/a')[0].text if get_xpath(self.dom, '//dd[@class="series"]//span[@class="position"]/a') else None

    # def authors(self):
        
    #     # self.author_name = [{"name": aut.text, "url": aut.attrib['href']} for aut in get_xpath(self.dom, '//*[@rel="author"]')]
    #     # self.author_url = [aut.attrib['href'] for aut in get_xpath(self.dom, '//*[@rel="author"]')]

    #     # author_list = []
    #     # for author in get_xpath(self.dom, '//*[@rel="author"]'):
    #     #     author_list.append({"name": author.text, "url": author.attrib['href']})
    #     return 
# fic = AO3Fic(get_page(URL2))
# print(vars(fic))

