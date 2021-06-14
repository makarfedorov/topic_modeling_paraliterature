import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import csv
from nltk.tokenize import word_tokenize 
import time
from nltk import download as nltk_download 
nltk_download ('punkt')
#PATH = ""
def ficbook(number, PATH_0, time_sleep = 0, genre = "", name = ""):
    number = number + 1
    id_n = 1
    fic = "https://ficbook.net"
    words = 0
    n_pages = 1
    age_group = ["G","PG-13","R","NC-17","NC-20"]
    romantics = ["Слэш", "Гет", "Джен", "Фемслэш", "Смешанная", "Другие виды отношений", "Статья"]
    states = ["Завершён","В процессе", "Заморожен"]
    headers={'User-Agent':'Mozilla/5.0'} 
    fw = open(name, 'w', newline='')
    fieldnames = ['id', 'author', "title", "link", "description", "tag", "likes", "date", "review", "size", "text", "rating", "parts", "romance", "fandom", "genre", "page"]
    writer = csv.DictWriter(fw, fieldnames=fieldnames)
    writer.writeheader()
    while id_n <= number:
        PATH = PATH_0 + str(n_pages) 
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
            status = []
            romance = ""
            fandom = []
            size = 0
            rating = []
            for i in soup_f.findAll("div", {"class":"creator-info"}):
                for a in i.findAll("a", {"class":"creator-nickname"}):
                    if a.has_attr("itemprop"):
                        authors.append(a.text)
                    elif a.has_attr("class") and str(a["class"]) == "creator-nickname" and i.find("i", {"class":"small-text text-muted"}).text == "соавтор":
                        authors.append(a.text)
              
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
            s = soup_f.find("section",{"class":"chapter-info"})
            rating = re.sub(r"\n", "", s.find("strong").text)
            
            for r in soup_f.findAll("span",{"class":"badge-text"}):
                if r.text in romantics:
                    romance = r.text
            for i in s.findAll("a"):
                if i.has_attr('href') and "/fanfiction/" in i["href"] and i.has_attr("class") and "js-open-notification-modal" in i["class"]:
                    fandom.append(i.text)     
            if len(fandom) == 1:
                fandom = fandom[0]  
            else:
                fandom = ",".join(fandom)    
            
                            
                
       
            size = len(word_tokenize(text))    
            if id_n < number:    
                writer.writerow({'id': id_n, 'author': authors, "title":title, "link":t["href"],"description":descr,"tag":",".join(tags),"likes":likes, "date":date, "review":n_reviews,"text":text, "rating": rating, "parts":parts, "romance":romance, "fandom":fandom, "size":size, "genre":genre, "page":n_pages})
                words += len(word_tokenize(text)) 
        
            id_n += 1
            if id_n >= number:
                break
            time.sleep(time_sleep)
        n_pages += 1
    fw.close() 
    return print(words)
