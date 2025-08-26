#import all needed modules
import requests, json, csv
from bs4 import BeautifulSoup

#fields for csv file
field_names = ['text', 'author', 'tags']

# get all data that you need
quotes = []
page = 1

while True:
    # get page

    html = requests.get(f'https://quotes.toscrape.com/page/{page}/')
    soup = BeautifulSoup(html.text, 'html.parser')

    # get data
    for line in soup.find_all('div', {'class':'quote'}):
        quote = {}
        quote['text'] = line.find('span',{'class':'text'}).text
        quote['author'] = line.find('small', {'itemprop':'author'}).text
        tags = [tag.text for tag in line.find_all('a', {'class': 'tag'})]  
        quote['tags'] = tags
        
        quotes.append(quote)
    
    # checking is there more pages to parse
    if soup.find('li', {'class': 'next'}):
        page += 1
    else:
        break

# create json file and adding data
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(quotes, f, indent=4, ensure_ascii=False)

# create csv file and adding data
with open('quotes.csv','w',newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader() 
    writer.writerows(quotes)

