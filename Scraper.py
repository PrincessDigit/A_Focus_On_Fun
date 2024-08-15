## Alastor Bloode 2024

## Simple web scraper

## Objective:
## To scrape data from a variety of sources for use in the training and classification systems. 

## Library of Congress URL (for scraping purposes): https://chroniclingamerica.loc.gov/search/pages/results/?state=&date1=1756&date2=1756&proxtext=&x=14&y=19&dateFilterType=yearRange&rows=20&searchType=basic

import requests #To grab images and news articles
from bs4 import BeautifulSoup  #To read the data gathered from the requests.
import fitz
import io
from PIL import Image
import os
class BloodeScraper:
    def __init__(self):
        self.path = None

    def data_organizer(self, year):
        p = os.path.join(os.curdir, str(year))

        if os.path.exists(p) == False:
            os.mkdir(p)
        self.path = p

    def Scrape_LoC(self, year1):
        ## Scraping data from the library of congress. Owing to newspapers not lining up anything, and the innaccuracies found in the
        ## currently transcribed text, I'm saving the images so I can train an object classifier. 
        self.data_organizer(year1)
        url = f"https://chroniclingamerica.loc.gov/search/pages/results/?state=&date1={year1}&date2={year1}&proxtext=&x=14&y=19&dateFilterType=yearRange&rows=20&searchType=basic"
        result = requests.get(url, 'html.parser')
        ## All we want is a PDF copy of the article. 
        soup = BeautifulSoup(result.content)
        divs = soup.find_all("div")
        urls = []
        LoC_base = "https://chroniclingamerica.loc.gov/"
        for d in divs:
                if d is None:
                     continue
                if "class" in d.attrs.keys():
                     if 'highlite' in d.attrs["class"]:
                        url = f"https://chroniclingamerica.loc.gov/{d.find('a')['href']}"
                        urls.append(url)
        
        ## What we gathered is the urls for all the images on the page.
        for url in urls:
             result = requests.get(url)
             url = BeautifulSoup(result.content, 'html.parser')
             title = url.title.text
             r = title.find(" «")
             title = title[:r]
             links = url.find_all("link")
             print(f"collecting {title}")
             path = os.path.join(self.path, f"{title}")
             for l in links:
                  if 'type' in l.attrs.keys():
                    if l.attrs['type'] == "application/pdf":
                        result = requests.get(f"{LoC_base}{l.attrs['href']}")
                        doc = fitz.Document(stream=result.content)
                        for page_index in range(len(doc)):
                            page = doc[page_index]
                            image_list = page.get_images(full=True)

                            if image_list:
                                print(f"[+] Found a total of {len(image_list)} images in page{page_index})")
                            else:
                                print(f"no pages found on page {page_index}")
                        
                        for image_index, img in enumerate(image_list, start=1):
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            image_ext = base_image["ext"]
                            image = Image.open(io.BytesIO(image_bytes))
                            path = path.replace("?", "x")
                            image.save(str(path+"."+image_ext))

if __name__ == "__main__":

    scraper = BloodeScraper()
    start = 1918
    end = 1924
    for i in range(start, end):
        scraper.Scrape_LoC(i)
