import requests
from bs4 import BeautifulSoup
import time
from go_excel_or_json import *

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.818 Yowser/2.5 Safari/537.36'
}

href = 'http://jansvarka.com.ua/ru/'
urls = []
csv_table = []
s = requests.get(url=href, headers=headers)
with open('index.html', encoding='utf-8', mode='w') as f:
    f.write(s.text)

with open('index.html', encoding='utf-8') as f:
    src = f.read()

page = BeautifulSoup(src, 'lxml')
all_urls_block = page.find(id='categories_block_left').find('ul')
my_block = all_urls_block.find_all('li')
# get all urls for categoties
for el in my_block:
    n = el.find('ul')
    if n != None:
        for a in n.find_all('li'):
            url = a.find('a').get('href')
            if url != '':
                urls.append(url)
# get all products urls
all_urls = []


def get_all_urls():
    global all_urls

    i = 0
    for url in urls:
        thing_page = requests.get(url=url, headers=headers).text
        page = BeautifulSoup(thing_page, 'lxml')
        page = page.find('ul', class_='product_list grid row')
        try:
            for card in page.find_all('div', class_='product-container'):  # find all cards with products on the page
                i += 1
                card_url = card.find('a', class_='product-name').get('href')  # get url of one card
                all_urls.append(card_url)
        except Exception as ex:
            print(ex)


def get_page_data(url):
    product_page = requests.get(url=url, headers=headers).text
    page = BeautifulSoup(product_page, 'lxml')

    # name find
    name = page.find(itemprop='name').text

    # img find
    img_link = page.find('img', id='bigpic').get('src')

    # cost find
    cost = page.find(id='our_price_display').text
    cost_value = page.find(id='our_price_display').text[0]

    # id find
    id = page.find(itemprop='sku').text

    # description find
    try:

        text = page.find('div', class_='b-user-content').text
    except Exception as ex:
        text = "Нет описания"
        print(f'[INFO] - у товара на странице {url} нет описания')


    # availability
    if page.find(id='availability_value').text == '':
        aval = 'Товар в наличии'
    else:
        aval = 'Товар ожидается'
    res = [name, img_link, cost[1::], cost_value, id, text, aval]
    # csv_table.append(res)
    return res


data = []
if __name__ == '__main__':
    with open('res.txt') as f:
        for line in f:
            data.append(get_page_data(line))
    with open('res_default.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(data)
