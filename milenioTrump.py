import requests_html
import json
import re
class MilenioTrump:
    def __init__(self, url, base_url="https://www.milenio.com/", results_dir=None):
        self.url = url
        self.base_url = base_url
        self.current_page = self.actual_page(url)
        self.html = self.get(url, self.current_page)
        self.results_dir = results_dir
        self.NEWS = None
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
    def _extractNewsFromCurrentPage(self):
        """
        Dada una pagina extraer multiples noticias
        y guardarlos en una lista
        Returns
        ------
            self.News: list
                Lista de diccionarios
        """
        print("Extracting news from page: ", self.current_page)
        news=self.html.find("div[class='list-news-container']",first=True)
        n=news.find("div[class='lr-row-news']")
        news=[self._extractSingleNew(x) for x in n]
        self.NEWS = news
    def _next_page(self):
        """
        Ir a la siguiente pagina de noticias
        ¿como sabemos que llegamos al final de las noticias?
        Si la siguiente pagina es menor que la pagina anterior!
        """
        nextPage = self.html.find("a[class='link-pagination']")[-1].links.pop()
        nextPageNumber = self.actual_page(nextPage)
        self.url = self.base_url+nextPage
        self.html = self.get(self.url, nextPageNumber)
        assert nextPageNumber > self.current_page, "Has llegado al final de las noticias"
        self.current_page = nextPageNumber
    def _saveNews(self):
        assert isinstance(self.NEWS, list)
        d = self.results_dir if "/" not in self.results_dir else self.results_dir.replace("/","")
        filename = f"{d}/news_page{self.current_page}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.NEWS, f, ensure_ascii=False, indent=2)
    def extractNews(self, n_pages):
        """
        Iterar sobre n paginas de noticias y guardar los resutlados.
        """
        for it in range(n_pages):
            self._extractNewsFromCurrentPage()
            self._saveNews()
            self._next_page()
        self._extractNewsFromCurrentPage()
        self._saveNews()

if __name__=="__main__":
    ### PARAMS ###
        # Pagina inicial
    url2="https://www.milenio.com/temas/donald-trump/"
    res_dir = "results/" # Directorio de resultados
    n = 5 # Numero de paginas a extraer
    ##############

    milenio=MilenioTrump(url2, results_dir=res_dir)
    milenio.extractNews(n)
