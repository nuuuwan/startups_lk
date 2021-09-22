import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from utils import jsonx

from startups_lk._constants import get_funding_stage_id, get_startup_stage_id
from startups_lk._utils import log

URL = 'https://www.startupsl.lk/masterSearchMainWindow'
TIME_WAIT = 20
DATA_FILE = '/tmp/startups_lk.json'


def scrape_and_dump():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(URL)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(TIME_WAIT)

    div_startups = driver.find_elements_by_xpath(
        "//*[@class='card container-fluid']"
    )
    data_list = []
    for div_startup in div_startups:
        a_name = div_startup.find_element_by_class_name('startup_name')
        name = a_name.text

        img = div_startup.find_element_by_tag_name('img')
        img_src = img.get_attribute('src')

        a_tagline = div_startup.find_element_by_class_name('startup_tagline')
        tagline = a_tagline.text

        p_description = div_startup.find_element_by_class_name('card-text')
        description = p_description.text

        a_url = div_startup.find_elements_by_class_name('startup_url')[1]
        url = a_url.get_attribute('href')

        div_detail = div_startup.find_element_by_class_name('div_detail')
        details = {}
        for div_column in div_detail.find_elements_by_class_name('flex-row'):
            k = None
            for div_info in div_column.find_elements_by_class_name('h8'):
                v = div_info.text
                if k is None:
                    k = v
                    details[k] = []
                else:
                    details[k].append(v)

        business_registration = details.get('Business Registration')[0]
        category = details.get('Startup Catogory')
        funding_stage = details.get('Funding Stage')[0]
        startup_stage = details.get('Startup Stage')[0]
        founder = details.get('Founder')

        data_list.append(
            dict(
                name=name,
                img=img_src,
                tagline=tagline,
                description=description,
                url=url,
                business_registration=business_registration,
                category=category,
                startup_stage=startup_stage,
                startup_stage_i=get_startup_stage_id(startup_stage),
                funding_stage=funding_stage,
                funding_stage_i=get_funding_stage_id(funding_stage),
                founder=founder,
            )
        )
        log.info(f'Wrote {name}')

    n_data_list = len(data_list)
    jsonx.write(DATA_FILE, data_list)
    log.info(f'Wrote {n_data_list} startups to {DATA_FILE}')
    driver.quit()


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
