#imports
from bs4 import BeautifulSoup 
import requests
import pandas as pd
import numpy as np


#obtain page links'    
def get_pages(main_url, start_page, end_page, http_headers):
        response = requests.get(main_url, headers = http_headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        page_link = soup.select_one('div.pagination__links > a')['href']
        pages = []
        for page_number in range(start_page, end_page+1):
                link = f"https://www.propertyfinder.eg/{page_link}&page={page_number}"
                pages.append(link)
        return pages


#get product from a page
def get_products(pages, http_headers):
        
        response = requests.get(pages, headers = http_headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        properties = soup.find_all("article", class_ = "card")
        for property in properties:           
                data['type'].append(property.find('p', class_='card-intro__type').text)
                
                data['location'].append(property.find('span', class_= 'card-specifications__location-text').text)
                
                data['price'].append(property.find('p', class_ = 'card-intro__price').text.replace(" ","").replace("EGP","").strip()) 
                
                data['link'].append(f"https://www.propertyfinder.eg{property.find('a')['href']}")
                
                for amenity in property.find_all('p', class_ = 'card-specifications__item'):
                        if 'sqm' in amenity.text.strip():
                                data['area'].append(amenity.text.strip().replace("sqm", ""))


#store data
def save_data(data):
        try : 
                df = pd.DataFrame(data)
                df.to_csv('C:\\Users\\k_abo\\Desktop\\Propertyfindder\\properties.csv')
        
        except :
                print('Missing value. Cannot save file!')



#main
if __name__ == '__main__':

        data = {
        'type': [],
        'location': [],
        'price': [],
        'area': [],
        'link': []
        }
        main_url = 'https://www.propertyfinder.eg/en/search?c=1&l=2254&ob=mr&page=1'
        http_headers =  {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,ar;q=0.7"}
        
        for page in get_pages(main_url = main_url, start_page = 1, end_page = 10, http_headers = http_headers):
                get_products(page, http_headers)
        save_data(data)