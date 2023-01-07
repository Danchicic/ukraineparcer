import time
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.818 Yowser/2.5 Safari/537.36'
}

href = 'http://jansvarka.com.ua/ru/'
urls = []


all_urls = []


def get_all_urls():
    global all_urls
    s = requests.get(url=href, headers=headers)

    page = BeautifulSoup(s.text, 'lxml')

    all_urls_block = page.find(id='categories_block_left').find('ul')
    my_block = all_urls_block.find_all('li')

    for el in my_block:
        n = el.find('ul')
        if n is not None:
            for a in n.find_all('li'):
                url = a.find('a').get('href')
                if url != '':
                    things_page = requests.get(url=url, headers=headers).text
                    page = BeautifulSoup(things_page, 'lxml')
                    for tag in page.find_all('a', class_='product-name'):
                        all_urls.append(f"{tag.get('href')}\n")
                    time.sleep(2)
    with open('res.txt', 'w') as f:
        f.writelines(all_urls)
    print(all_urls)


if __name__ == '__main__':
    get_all_urls()
