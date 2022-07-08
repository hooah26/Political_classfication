from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

df_total = pd.DataFrame()
category = ['bobae', 'mlb']

board = []

for i in range(853, 854):
    try:
        url = 'https://www.ppomppu.co.kr/zboard/view.php?id=pol_left&page=1&divpage=1&no={}'.format(i)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}
        res = requests.get(url, headers=headers)
        html = res.content.decode('euc-kr', 'replace')
        res.raise_for_status()
        soup = BeautifulSoup(html, 'html.parser')
        # title_t = soup.find("div", {"class": "titles"}).get_text()
        # content_t = soup.find("td", {"class": "board-contents"})
        content_t = soup.find.board-contents.p
        print(content_t)
        # if "정치" in title_t :
        #     total = title_t + ' ' + content_t
        #     board.append(re.compile('[^가-힣a-zA-Z ]').sub(' ', total))
        #     print(total)


        # else :
        #     continue
    except:
        print('error', i)



# print(len(mlb))
# df_mlb = pd.DataFrame({'title':mlb})
# df_mlb['category'] = 'mlb'
#
# print(df_mlb.head())
# df_mlb.to_csv('./mlb.csv', index=False)


# df_total = pd.concat([df_bobae, df_mlb],axis='rows', ignore_index=True)