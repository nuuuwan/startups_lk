import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import dt, filex, jsonx, timex, www

from startups_lk._constants import (DIR_IMAGE, REMOTE_DATA_DIR,
                                    URL_DATA_SOURCE, get_funding_stage_i,
                                    get_startup_stage_i)
from startups_lk._utils import log

TIME_WAIT = 20
HTML_FILE = '/tmp/startups_lk.html'
DATA_FILE = '/tmp/startups_lk.json'


def get_startup_id(name):
    return dt.to_kebab(name)


def parse_founder_info(founder_info_list):
    founder_info = {}
    for i, founder_info_list_item in enumerate(founder_info_list):
        if '@' in founder_info_list_item:
            founder_info['email'] = founder_info_list_item
        elif (
            founder_info_list_item[0] == '0'
            and len(founder_info_list_item) == 10
        ):
            founder_info['phone'] = founder_info_list_item
        else:
            founder_info['name'] = founder_info_list_item
    return founder_info


def download_html():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    log.info(f'Opening {URL_DATA_SOURCE}...')
    driver.get(URL_DATA_SOURCE)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(TIME_WAIT)

    html = driver.page_source
    filex.write(HTML_FILE, html)
    n_html_m = len(html) / 1_000_000
    log.info(f'Wrote {n_html_m}MB to {HTML_FILE}')
    driver.quit()


def parse_and_dump():
    html = filex.read(HTML_FILE)
    soup = BeautifulSoup(html, 'html.parser')

    div_startups = soup.find_all('div', class_='card container-fluid')
    data_list = []
    for div_startup in div_startups:
        a_name = div_startup.find('a', class_='startup_name')
        name = a_name.text
        startup_id = get_startup_id(name)

        img = div_startup.find('img')
        remote_img_url = img.get('src')

        a_tagline = div_startup.find('a', class_='startup_tagline')
        tagline = a_tagline.text
        p_description = div_startup.find('p', class_='card-text')
        description = p_description.text

        a_url = div_startup.find('a', class_='startup_url')
        url = a_url.get('href')

        div_detail = div_startup.find('div', class_='div_detail')
        details = {}
        for div_column in div_detail.find_all('div', class_='flex-row'):
            k = None
            for div_info in div_column.find_all('div', class_='h8'):
                v = div_info.text
                if k is None:
                    k = v
                    details[k] = []
                else:
                    details[k].append(v)

        business_registration_date = details.get('Business Registration')[0]
        business_registration_ut = (
            timex.parse_time(business_registration_date, '%Y-%m-%d')
            if business_registration_date != '-'
            else -1
        )
        category_list = details.get('Startup Catogory')
        funding_stage = details.get('Funding Stage')[0].strip()
        startup_stage = details.get('Startup Stage')[0].strip()
        founder_info_list_raw = details.get('Founder')
        founder_info = parse_founder_info(founder_info_list_raw)

        image_file_only = f'image.{startup_id}.png'

        data_list.append(
            dict(
                startup_id=startup_id,
                name=name,
                remote_img_url=remote_img_url,
                image_file_only=image_file_only,
                tagline=tagline,
                description=description,
                url=url,
                business_registration_date=business_registration_date,
                business_registration_ut=business_registration_ut,
                category_list=category_list,
                startup_stage=startup_stage,
                startup_stage_i=get_startup_stage_i(startup_stage),
                funding_stage=funding_stage,
                funding_stage_i=get_funding_stage_i(funding_stage),
                founder_info=founder_info,
                founder_info_list_raw=founder_info_list_raw,
            )
        )

    n_data_list = len(data_list)
    jsonx.write(DATA_FILE, data_list)
    log.info(f'Wrote {n_data_list} startups to {DATA_FILE}')


def download_images():
    if not os.path.exists(DIR_IMAGE):
        os.system(f'mkdir {DIR_IMAGE}')
    data_list = jsonx.read(DATA_FILE)
    for data in data_list:
        image_file_only = data['image_file_only']
        image_file = os.path.join(
            DIR_IMAGE,
            image_file_only,
        )
        if os.path.exists(image_file):
            log.warning(f'{image_file} exists')
            continue
        github_image_url = os.path.join(
            REMOTE_DATA_DIR,
            'startups_lk-images',
            image_file_only,
        )
        if www.exists(github_image_url):
            log.warning(f'{github_image_url} exists')
            continue
        data['image_file_only']
        remote_img_url = data['remote_img_url']

        os.system(
            'wget --no-check-certificate '
            + f'-O "{image_file}" "{remote_img_url}"'
        )


def load_startups(min_funding_stage_i=-1, min_startup_stage_i=-1):
    data_list = jsonx.read(DATA_FILE)
    if min_funding_stage_i != -1:
        data_list = list(
            filter(
                lambda data: data['funding_stage_i'] >= min_funding_stage_i,
                data_list,
            )
        )
    if min_startup_stage_i != -1:
        data_list = list(
            filter(
                lambda data: data['startup_stage_i'] >= min_startup_stage_i,
                data_list,
            )
        )
    return data_list


if __name__ == '__main__':
    download_html()
    parse_and_dump()
    download_images()
