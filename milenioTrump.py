import requests_html
import json
import re

class MilenioTrump:
    def __init__(self, url):
        self.url = url
        self.current_page = self.actual_page(url)
        self.html = self.get(url, self.current_page)
    @staticmethod
    def get(url, n_page):
        """
        Hacer request a la pagina y devolver el html
        En caso de estatus diferente de 200 marca AssertError
        """
        header={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "Upgrade-Insecure-Requests": "1",
            "Referer": f"https://www.milenio.com/temas/donald-trump/page/{n_page-1 if n_page>1 else 1}?",
            "Host": "www.milenio.com"
        }
        print("Header ", header["Referer"])
        sess=requests_html.HTMLSession()
        page=sess.get(url, headers=header)
        assert page.status_code==200, f"Bad Response From Page; STATUS={page.status_code}"
        print("Extracting from ",page.url)
        return page.html
    @staticmethod
    def _extractSingleNew(n):
        """Extrae el contenido de la noticia
            Input:
                n:html que contiene la info de la noticia
            Output:
                Regresa un json con la información"""
        date,title,info=n.text.split("\n")
        link=n.links.pop()
        photo=n.find("img",first=True).attrs["src"]
        return {
            "titulo":title,
            "fecha":date,
            "foto":photo,
            "liga":link,
            "intro":info
        }
    @staticmethod
    def actual_page(url):
        """
        Dada una url, devuelve la pagina actual en la que estamos.
        """
        curr = re.search("(\d+)",url)
        if curr:
            page = int(curr.groups()[0])
        else:
            page=1
        return page
    def extractNews(self):
        """
        Dada una pagina extraer multiples noticias
        """
        print("Extracting news from page: ", self.current_page)
        news=self.html.find("div[class='list-news-container']",first=True)
        n=news.find("div[class='lr-row-news']")
        news=[self._extractSingleNew(x) for x in n]
        return news
