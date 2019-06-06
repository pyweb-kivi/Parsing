#scrap leemarpet.com

import requests
from selenium import webdriver
from time import sleep
import csv

def read_file():
    """Чтение из файла"""
    try:
        with open('test.txt', 'r+', encoding = 'UTF-8') as codes:
            array = [row.strip() for row in codes]
        return array

    except IOError as err:
        print(u'Can\'t open the "{0}" file'.format(err.filename))

def write_csv(data):
    """Запись .csv"""
    with open('imgs.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow( (data['img'],
						  data['url']) )

'''
def status_code(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.Timeout:
        print('Timeout')
    except requests.HTTPError as err:
        code = err.response.status_code
        print('Page error')
    except requests.RequestException:
        print('URL error')
'''

def main():
    #url = 'http://www.leemarpet.com/'
    driver = webdriver.Firefox() #Chrome(executable_path=r"C:\chromedriver_win32\chromedriver.exe") #или Firefox()
    driver.get('http://www.leemarpet.com/')
    sleep(1)
    driver.find_elements_by_xpath("//div[@id='welcome-pop']/div")
    skip = driver.find_elements_by_xpath("//div[@id='welcome-pop']/div")[-1].find_element_by_xpath('a').click()
    bar_code_list = read_file()
    for i in bar_code_list:
        try:
            sleep(1)
            res_search = driver.find_element_by_xpath("//div[@class='searchBox no-checkout']//div[@class='Putter']/input").send_keys(i)
            button = driver.find_element_by_xpath("//button[@class='Submit SubmitSEARCH']").click()
            product_click = driver.find_element_by_xpath("//div[@class='image-space product_thumb_container']").click()
            sleep(2)
            url_view_image = driver.find_element_by_xpath("//div[@id='main_image_zoom']/a").get_attribute("href")
            name = i + '.jpg'
        except:
            name = i + '.jpg'
            url_view_image = 'ERROR'

        data = {'img': name,
                'url': url_view_image}
        write_csv(data)
    driver.close()

if __name__ == '__main__':
    main()
