import requests
import openpyxl
from bs4 import BeautifulSoup
import openpyxl


def write_to_table(row_num, date):
    wb = openpyxl.load_workbook(filename='openpyxl.xlsx')
    sheet = wb['Лист1']
    print(row_num)
    sheet[f'A{row_num}'] = date[0]
    sheet[f'B{row_num}'] = date[1]
    sheet[f'C{row_num}'] = date[2]
    sheet[f'D{row_num}'] = date[3]
    sheet[f'E{row_num}'] = date[4]
    sheet[f'F{row_num}'] = date[5]
    wb.save('openpyxl.xlsx')


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.3.818 Yowser/2.5 Safari/537.36'
}

href = 'http://jansvarka.com.ua/ru/'
urls = []

# s = requests.get(url=href, headers=headers)
# with open('index.html', encoding='utf-8', mode='w') as f:
#     f.write(s.text)

i = 0
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

for url in urls:

    # thing_page = requests.get(url=url, headers=headers).text
    # page = BeautifulSoup(thing_page, 'lxml')

    # with open('index2.html', mode='w', encoding='utf-8') as f:
    #     f.write(thing_page.text)
    # with open('index2.html', encoding='utf-8') as f:
    #     src = f.read()
    # page = BeautifulSoup(src, 'lxml')

    page = page.find('ul', class_='product_list grid row')

    for card in page.find_all('div', class_='product-container'):  # find all cards with product's on the page
        i += 1
        # card url find
        card_url = card.find('a', class_='product-name').get('href')  # get url of one card

        product_page = requests.get(url=card_url, headers=headers).text
        page = BeautifulSoup(product_page, 'lxml')

        # with open('index3.html', mode='w', encoding='utf-8') as f:
        #     f.write(product_page.text)
        # with open('index3.html', encoding='utf-8') as f:
        #     src = f.read()
        # page = BeautifulSoup(src, 'lxml')



        # name find
        name = page.find(itemprop='name').text

        # img find
        img_link = page.find('img', id='bigpic').get('src')

        # cost find
        cost = page.find(id='our_price_display').text
        cost_value = page.find(id='our_price_display').text[0]

        # 5 ???? 5 ??????? 5 ?????? 5 ???

        # id find
        id = page.find(itemprop='sku').text

        # description find
        text = page.find('div', class_='b-user-content').text

        # availability
        if page.find(id='availability_value').text == '':
            aval = 'Товар в наличии'
        else:
            aval = 'Товар ожидается'
        res = [name, img_link, cost[1::], cost_value, id, text, aval]
        print(res)
        write_to_table(i, res)
    break
