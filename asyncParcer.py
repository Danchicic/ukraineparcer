import requests
from bs4 import BeautifulSoup
import time
from go_excel_or_json import *
import asyncio
import aiohttp

urls = []
data = []


async def get_page_data(session, url, i):
    global data
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'ru,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.818 Yowser/2.5 Safari/537.36'
    }
    async with session.get(url=url, headers=headers) as response:
        response_text = await response.text()
        page = BeautifulSoup(response_text, 'lxml')

        # name find
        try:
            name = page.find(itemprop='name').text
        except Exception as ex:
            name = "Нет Имени"
            print(f'[INFO] - у товара на странице {url} нет Имени?')

        # img find
        try:
            img_link = page.find('img', id='bigpic').get('src')
        except Exception as ex:
            img_link = "Нет Картинки"
            print(f'[INFO] - у товара на странице {url} нет Картинки')

        # cost find
        try:
            cost = page.find(id='our_price_display').text
            cost_value = page.find(id='our_price_display').text[0]
        except Exception as ex:
            cost = "Нет цены"
            cost_value = '-'
            print(f'[INFO] - у товара на странице {url} нет цены')

        # id find
        try:
            id = page.find(itemprop='sku').text
        except Exception as ex:
            id = "Нет Артикула"
            print(f'[INFO] - у товара на странице {url} нет артикула')

        # description find
        try:
            text = page.find('div', class_='b-user-content').text
        except Exception as ex:
            text = "Нет описания"
            print(f'[INFO] - у товара на странице {url} нет описания')

        # availability
        try:
            if page.find(id='availability_value').text == '':
                aval = 'Товар в наличии'
            else:
                aval = 'Товар ожидается'
        except:
            aval = 'Нет'
            print('Нет наличия')

        res = [name, img_link, cost[1::], cost_value, id, text, aval]
        data.append(res)
    print(f"[INFO] Обработал страницу {i} \ 900")


async def gather_data():
    async with aiohttp.ClientSession() as Session:
        tasks = []
        with open('res.txt') as f:
            for line in f:
                urls.append(line[:-1])

        for i in range(1, len(urls) + 1):
            task = asyncio.create_task(get_page_data(Session, urls[i - 1], i))
            tasks.append(task)

        await asyncio.gather(*tasks)


def main():
    asyncio.run(gather_data())
    with open('res_async.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
