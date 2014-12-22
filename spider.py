import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib import parse
from website import Page, Site
from sqlalchemy.orm import Session
from connection import Base, engine


class Spider():
    def __init__(self, domain, domain_id, session):
        self.scaned_url = []
        self.domain = domain
        self._domain_id = domain_id
        self._session = Session(bind=session)
        self.to_scan = []

    def from_href_to_url(self, href, url):
        return parse.urljoin(url, href)

    def is_outgoing(self, url):
        obj = urlparse(url)
        if obj.netloc == self.domain and '#' not in url:
            return False
        return True

    def save_page_in_DB(self, soup, url):
        try:
            desc = self.soup.find(attrs={"property": "og:description"}).get("content")
        except Exception as e:
            desc = ""
        new_page = Page(title=soup.title.string,
                        description=desc,
                        url=url,
                        website=self._domain_id)
        self._session.add(new_page)
        self._session.commit()

    def scan_page(self, url):
        if url in self.scaned_url:
            return
        print(url)
        self.scaned_url.append(url)
        my_request = requests.get(url)
        html = my_request.text
        soup = BeautifulSoup(html)
        try:
            self.save_page_in_DB(soup, url)
        except Exception as e:
            print(e)
        all_links = soup.find_all('a')
        for link in all_links:
            href = link.get('href')
            next_page = self.from_href_to_url(href, url)
            if next_page not in self.scaned_url and not self.is_outgoing(next_page):
                self.to_scan.append(next_page)
                
    def scan_site(self):
        url = "http://" + self.domain
        self.scan_page(url)
        while len(self.to_scan) != 0:
            self.scan_page(self.to_scan.pop())

            
def save_site(url, session):
    n_session = Session(bind=session)
    new_site = Site(url=url)
    n_session.add(new_site)
    n_session.commit()
    my_domain_id = n_session.query(Site.id).filter(Site.url == url).all()
    return my_domain_id

if __name__ == '__main__':
    url = "boredpanda.com"
    m_engine = engine
    Base.metadata.create_all(engine)
    my_domain_id = save_site("http://{}".format(url), m_engine)
    domain = Spider(url, my_domain_id[0][0], engine)
    domain.scan_site()
