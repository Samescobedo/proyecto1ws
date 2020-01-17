import requests_html
import json

sess=requests_html.HTMLSession()

url="https://www.milenio.com/temas/donald-trump"
page=sess.get(url)
page.status_code

news=page.html.find("div[class='list-news-container']",first=True)
news

n=news.find("div[class='lr-row-news']")
n

link=n.links.pop()

def extracNews (n):
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

#Resultado
res=[extracNews(x) for x in n]
res

with open ("Noticias_Milenio.json","w",encoding="utf-8") as f:
    #json.dump para crear json
    json.dump(res,f, ensure_ascii=False, indent=2)
