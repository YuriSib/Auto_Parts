import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import urllib.request

from excel_master import create_column, import_xl, property_export


def settings(url_):
    ua = UserAgent()
    user_agent = ua.random
    headers = {'User-Agent': user_agent}
    response = requests.get(url_, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def property_scrapper(url_, table):
    soup = settings(url_)

    html_property_ = soup.find_all('span', {'class': 'filter_title'})
    property_ = ['Наименование'] + [i.get_text(strip=True) for i in html_property_ if 'Модели' not in i] + ['Фото']

    create_column(table, property_)

    return property_


def photo_saver(url_, name):
    try:
        urllib.request.urlopen(url_)
    except urllib.error.URLError as e:
        print("Ошибка при скачивании фото:", e)
    else:
        with open(f'фото\{name}.jpg', 'wb') as f:
            f.write(urllib.request.urlopen(url_).read())
            print("Фото успешно скачано!")


def link_scrapper(url_):
    product_list = []
    nums = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']

    session = HTMLSession()

    for num in nums:
        parts = url_.split('&')
        parts[2] = f'start={num}'
        url_ = '&'.join(parts)

        r = session.get(url_)
        r.html.render()
        soup = BeautifulSoup(r.text, 'lxml')

        html_product = soup.find('ul', {'class': 'item_ul'}).find_all('li', {'class': 'item'})

        name_n_brand_n_link_n_photo_list = []
        for i in html_product:
            name = i.find('p').get_text(strip=True)
            brand = i.find('h3').get_text(strip=True)
            link = 'https://all-world-cars.com' + i.find('p').a['href']
            photo = 'https:' + i.find('div', {'class': 'article-image'}).find('img')['src']

            name_n_brand_n_link_n_photo_list.append((name, brand, link, photo))

        if name_n_brand_n_link_n_photo_list[0] not in product_list:
            product_list.extend(name_n_brand_n_link_n_photo_list)
        else:

            break
    return product_list


def product_scrapper(url_, name, brand, photo):
    soup = settings(url_)

    html_property_ = soup.find_all('div', {'class': 'characteristicsListRow'})
    property_list = [(prp.find_all('span')[0].get_text(strip=True)[:-1], prp.find_all('span')[1].get_text(strip=True))
                     for prp in html_property_]
    property_list = [('Наименование', name)] + [('Бренды', brand)] + property_list + ['Фото', photo]

    return property_list


def main(table, url_):
    property_scrapper(url_, table)
    link_list = link_scrapper(url_)

    count = 2
    for link in link_list:
        property_list_ = product_scrapper(link[2], link[0], link[1], link[3])
        try:
            photo_saver(link[3], link[0])
        except FileNotFoundError:
            print(f'На {count} строке возникла ошибка, строка будет пропущена!')
            continue

        property_export(row=count, table=table, site_prop_list=property_list_)
        count += 1
        print(count)


if __name__ == "__main__":
    list_catalog = [
        ('Моторное масло', 'https://all-world-cars.com/oils_catalog'),
        ('Тормозные жидкости', 'https://all-world-cars.com/brake_fluids_catalog'),
        ('Присадки1', 'https://all-world-cars.com/oil_additives_catalog'),
        ('Присадки2', 'https://all-world-cars.com/fuel_additives_catalog'),
        ('Присадки3', 'https://all-world-cars.com/cooling_system_additives_catalog'),
        ('Антифриз', 'https://all-world-cars.com/coolant_catalog?goods_group=coolant&action=search&viewMode=tile&prope'
                      'rty%5Bcoolant_type%5D%5B%5D=antifreeze&property%5Bliquid_volume%5D%5Bfrom%5D=&property%5Bliquid_'
                      'volume%5D%5Bto%5D=&property%5Bfrost_temp%5D%5Bfrom%5D=&property%5Bfrost_temp%5D%5Bto%5D=&proper'
                      'ty%5Bboil_temp%5D%5Bfrom%5D=&property%5Bboil_temp%5D%5Bto%5D='),
        ('Смазки', 'https://all-world-cars.com/lubricants_catalog'),
        ('Провода пусковые', 'https://all-world-cars.com/jumper_cables_catalog'),
        ('Ароматизаторы', 'https://all-world-cars.com/car_freshners_catalog'),
        ('Инструменты1', 'https://all-world-cars.com/tool_sets_catalog'),
        ('Инструменты2', 'https://all-world-cars.com/sockets_catalog'),
        ('Инструменты3', 'https://all-world-cars.com/clamps_catalog'),
        ('Инструменты4', 'https://all-world-cars.com/lug_wrenches_catalog'),
        ('Аккумуляторы', 'https://all-world-cars.com/batteries_catalog'),
        ('Шины', 'https://all-world-cars.com/tires_catalog'),
        ('Диски', 'https://all-world-cars.com/disks_catalog'),
        ('Автохимия', 'https://all-world-cars.com/ext_cleaners_catalog'),
        ('Щетки стеклоочистителя', 'https://all-world-cars.com/wipers_catalog'),
        ('Домкрат', 'https://all-world-cars.com/jacks_catalog'),
        ('Герметики', 'https://all-world-cars.com/sealants_catalog'),
        ('Пусковое устройство', 'https://all-world-cars.com/battery_boosters_catalog'),
        ('Ремни', 'https://all-world-cars.com/poly_v_belts_catalog'),
        ('Очистка льда и снега', 'https://all-world-cars.com/brushes_scrapers_catalog'),
        ('Троса', 'https://all-world-cars.com/towing_ropes_catalog'),
        ('Аптечки', 'https://all-world-cars.com/first_aid_kit_catalog'),
        ('Жилеты', 'https://all-world-cars.com/emergency_waistcoats_catalog'),
        ('Стеклоомывайка', 'https://all-world-cars.com/washer_liquids_catalog')
    ]
    for category in list_catalog:
        # categories_url = 'https://all-world-cars.com/oils_catalog?goods_group=oils&limit=100&start=00'
        categories_url = category[1] + '?limit=100&start=00'
        table = f'{category[0]} + .xlsx'
        main(table, categories_url)
    #
    # link_scrapper(url)
    url = 'https://all-world-cars.com/parts/LUKOIL/3148675?source=oils_catalog'
    # property_list = product_scrapper(url)
    main('Каталог.xlsx', categories_url)
