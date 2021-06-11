import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import csv
from nltk.tokenize import word_tokenize 
import time
from nltk import download as nltk_download 
nltk_download ('punkt')
#PATH = "https://ficbook.net/find?fandom_filter=any&fandom_group_id=1&pages_range=3&pages_min=0&pages_max=20&statuses%5B0%5D=1&statuses%5B1%5D=2&sizes%5B0%5D=2&ratings%5B0%5D=5&ratings%5B1%5D=6&ratings%5B2%5D=7&ratings%5B3%5D=8&ratings%5B4%5D=9&transl=3&directions%5B0%5D=1&tags_include%5B0%5D=1665&likes_min=&likes_max=&date_create_min=2021-05-10&date_create_max=2021-05-10&date_update_min=2021-05-10&date_update_max=2021-05-10&title=&sort=1&rnd=1786303482&find=%D0%9D%D0%B0%D0%B9%D1%82%D0%B8!&p="
def ficbook(number, PATH, time_sleep = 0, genre = "", name = ""):
    id_n = 1
    fic = "https://ficbook.net"
    words = 0
    n_pages = 1
    age_group = ["G","PG-13","R","NC-17","NC-20"]
    romantics = ["Слэш", "Гет", "Джен", "Фемслэш", "Смешанная", "Другие виды отношений", "Статья"]
    states = ["finished","frozen", "in-progress"]
    headers={'User-Agent':'Mozilla/5.0'} 
    fw = open(name, 'w', newline='')
    fieldnames = ['id', 'author', "title", "link", "description", "tag", "likes", "date", "review", "size", "text", "rating", "status", "parts", "romance", "fandom", "genre"]
    writer = csv.DictWriter(fw, fieldnames=fieldnames)
    writer.writeheader()
    while words < number:
        PATH = PATH + str(n_pages) 
        request=urllib.request.Request(PATH,None,headers)
        markup = urllib.request.urlopen(request)
        soup = BeautifulSoup(markup)
        l = []
        for t in soup.findAll("a", {"class":"visit-link"}):
            if "source=premium" in t["href"]:
                continue
            new_path = fic +  t["href"]   
            new_request=urllib.request.Request(new_path,None,headers)
            f_html = urllib.request.urlopen(new_request)
            soup_f = BeautifulSoup(f_html)
            authors = []
            tags = []
            n_reviews = 0
            descr = ""
            date = ""
            format = ""
            likes = 0
            parts = []
            parts_link = []
            text = ""
            title = ""
            rating = ""
            status = ""
            romance = ""
            fandom = []
            size = 0
            for n in soup_f.findAll("a", {"class":"creator-nickname"}):
                authors.append(n.text)
            if len(authors) == 1:
                authors = authors[0]
            elif len(authors) > 1: 
                authors = ",".join(authors)
            for tag in soup_f.findAll("a", {"class":"tag"}):
                tags.append(tag.text)
            review_link = t["href"]+ "/" + "comments#content"
            for n in soup_f.findAll("a", {"href":review_link}):
                n_reviews = int(n.span.text)
            for d in soup_f.findAll("div", {"itemprop":"description"}):  
                descr = d.text
            for dat in soup_f.findAll("div", {"class":"part-date"}):  
                date = dat["content"]
            for forma in soup_f.findAll("span", {"class":"js-link"}): 
                format = re.sub(r'\n', r'', forma.text)
                format = re.sub(r'\s', r'', forma.text)
            for like in soup_f.findAll("span", {"class":"badge-text js-marks-plus"}):
               likes = int(like.text)
            if len(soup_f.findAll("div", {"id":"content"})) >= 1:
                parts = "Нет"
                for tex in soup_f.findAll("div", {"itemprop":"articleBody"}):
                    text = tex.text
            
            else:
                for lin in soup_f.findAll("a", {"class":"part-link visit-link "}): 
                    parts_link.append(lin["href"])
                    parts = ",".join(parts_link)
                    for part_link in  parts_link:
                        new_new_path = fic + part_link
                        new_new_request=urllib.request.Request(new_new_path,None,headers)
                        p_html = urllib.request.urlopen(new_new_request)
                        soup_p = BeautifulSoup(p_html)
                        for p_text in soup_p.findAll("div", {"itemprop":"articleBody"}):
                            text = text + p_text.text
            for titl in soup_f.findAll("h1", {"class":"mb-10"}): 
                title = titl.text
            for age in age_group:
                for ag in soup_f.findAll("strong",{"class":"badge-with-icon badge-rating-" + age}):
                    rating = re.sub(r"\n",r"", ag.text)
            for r in soup_f.findAll("span",{"class":"badge-text"}):
                if r.text in romantics:
                    romance = r.text
            for a in soup_f.findAll("a"):  
                if a.has_attr('href') and "/fanfiction/" in a["href"]:
                    fandom.append(a.text)     
            fandom = set(fandom) 
            fandom = list(fandom)  
            if len(fandom) == 1:
                fandom = fandom[0]  
            else:
                fandom = ",".join(fandom)             
            for state in states:
                for st in soup_f.findAll("span",{"class":"badge-with-icon badge-secondary badge-status-" + state}):
                    status = re.sub(r"\n", "", st.text)
            writer.writerow({'id': id_n, 'author': authors, "title":title, "link":t["href"],"description":descr,"tag":",".join(tags),"likes":likes, "date":date, "review":n_reviews,"text":text, "rating": rating, "status":status, "parts":parts, "romance":romance, "fandom":fandom, "size":size, "genre":genre})
            words += len(word_tokenize(text)) 
            size = word_tokenize(text)
        
            id_n += 1
            n_pages += 1
            if words >= 300000:
                break
            time.sleep(time_sleep)
    fw.close() 
