from selenium import webdriver
from selenium.webdriver.firefox.options import Options

URL = 'https://www.startupsl.lk/masterSearchMainWindow'


def scrape():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    div_startups = driver.find_elements_by_class_name('card container-fluid')
    for div_startup in div_startups:
        print(div_startups)
        break

    driver.get(URL)
    driver.quit()


if __name__ == '__main__':
    scrape()
