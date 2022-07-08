from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from lxml import etree

df_total = pd.DataFrame()
category = ['bobae', 'mlb']

titles = []
contents = []

for i in range(555383, 585383):
    try:
        url='https://www.bobaedream.co.kr/view?code=politic&No={}&bm=1'.format(i)
        headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
        res = requests.get(url, headers=headers)
        html = res.content.decode('utf-8','replace')
        res.raise_for_status()
        soup = BeautifulSoup(html,'html.parser')
        title_t = soup.find("strong",{"itemprop":"name"}).get_text()
        content_t = soup.find("div",{"class":"bodyCont"}).get_text()
        titles.append(re.compile('[^가-힣a-zA-Z ]').sub(' ', title_t))
        contents.append(re.compile('[^가-힣a-zA-Z ]').sub(' ', content_t))
    except:
        print('error', i)

print(len(titles))
print(len(contents))
df_bobae = pd.DataFrame({'title':titles, 'contents':contents})
df_bobae['category'] = 'bobae'

print(df_bobae.head())
df_bobae.to_csv('./bobae.csv', index=False)


# df_total = pd.concat([df_bobae, df_mlb],axis='rows', ignore_index=True)


