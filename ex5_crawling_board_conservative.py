from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time

option = webdriver.ChromeOptions()
#options.add_argument('headless')
option.add_argument('lang=ko_KR')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=option)
driver.implicitly_wait(10)

category = ['bobae', 'mlb']

title_list = []
df_title = pd.DataFrame()
for i in range(904, 1017):
    url = 'https://www.ppomppu.co.kr/zboard/view.php?id=pol_right&page=1&divpage=1&no={}'.format(i)
    driver.get(url)
    #time.sleep(0.5)
    try:
        title = driver.find_element_by_xpath('/html/body/div/div[2]/div[5]/div/table[5]/tbody/tr[1]/td/table/tbody/tr/td/table').text
        # print(title)
        title = re.compile('[^가-힣a-zA-Z ]').sub(' ', title)
        title_list.append(title)
    except StaleElementReferenceException:
        driver.get(url)
        time.sleep(0.5)
    except:
        print('error')
# print(title_list)
df_title = pd.DataFrame(title_list, columns=['title'])
df_title['category'] = 'mlb'
# df_title = pd.concat([df_title, df_contents],
#                      axis='rows', ignore_index=True)
driver.close()
df_title.info()
print(df_title)
print(df_title.category.value_counts())
df_title.to_csv('./data/board_conservative.csv', index=False)
