import sys
import os
import csv
import json
import requests
from bs4 import BeautifulSoup


class Scraper:
    # python script.py source.csv
    # sys.argv[1]  --- returns ---> source.csv
    def get_input_csv_file(self):
        if len(sys.argv) <= 1:
            raise Exception('Please provide csv file!')

        return sys.argv[1]

    def get_urls_from_csv_file(self, csv_file):
        urls = []

        if os.path.isfile(csv_file) == False:
            raise Exception('Please provide valid csv file!')

        with open(csv_file, 'r', newline='') as fh:
            reader = csv.reader(fh)
            for row in reader:
                urls.append(row[0])

        return urls

    def scrape(self, urls):
        watches = []

        if len(urls) == 0:
            raise Exception('CSV file is empty or format is not correct!')

        for url in urls:
            response = requests.get(url)
            watch_html = response.text

            soup = BeautifulSoup(watch_html, 'html.parser')

            # title
            title = soup.find(
                'div', {'class': 'product-information-wrapper'}).find('h1').span.text
            # print (title)

            # price
            price = soup.find(
                'div', {'class': 'product-price'}).find('span').text
            # print(price)
            # price = price.split(' ')[0]

            # code
            code = soup.find('div', {'class': 'code'}).find('span').text
            # print (code)

            # category
            category = soup.find('table', {'class': 'table'}).find(
                'tr', {'class': 'attr-brend'}).text
            # print(category)

            # image
            # image = soup.css.select('img.img-responsive')
            # image = image[0]['src']

            image = soup.select_one('.item img')['src']
            # print(image)

            watch = {'title': title, 'price': price,
                     'category': category, 'image': image, 'code':code}

            watches.append(watch)

        return watches

    def store_watches_to_json(self, watches):
        if len(watches) <= 0:
            raise Exception('Product list is empty!')

        watches_json = json.dumps(watches)

        with open('watches/watches.json', 'w') as fh:
            fh.write(watches_json)
            print('Saved!')
