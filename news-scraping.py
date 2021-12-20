from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import xlsxwriter

#Variables
newsList=[]
contentsList=[]
titleNews_onlytext=[]
contentNews_onlytext=[]
linkstoNews_list=[]
file_name='Ultimas_Noticias.xlsx'


def innerHTML(element):
    return element.encode_contents()



try:
    url = urlopen("https://g1.globo.com/ultimas-noticias/")
except HTTPError as error:
    print(error)
except URLError as error:
    print(error)
else:
    html = BeautifulSoup(url.read(),"html.parser")
    
    titleNews = html.find_all("a", {"class": "feed-post-link gui-color-primary gui-color-hover"})
    for i in titleNews:
        titleNews_onlytext.append(innerHTML(i))
    for i in titleNews_onlytext:
            newsList.append(i.decode("utf-8", "strict"))

    

    linkstoNews = html.find_all("a", {"class": "feed-post-link gui-color-primary gui-color-hover"})
    for i in linkstoNews:
        linkstoNews_list.append(i['href'])
    

    

    contentNews = html.find_all("div", {"class": "feed-post-body-resumo"})
    for r in contentNews:
        contentNews_onlytext.append(innerHTML(r))
    for r in contentNews_onlytext:
        contentsList.append(r.decode("utf-8", "strict"))
    
    data = {'News': newsList, 'Contents':contentsList, 'Links': linkstoNews_list}
    dfNews= pd.DataFrame(data)
    dfNews.to_excel(file_name,sheet_name='Sheet1')
   


    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    
        dfNews.to_excel(excel_writer=writer)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        for i, col in enumerate(dfNews.columns):
            column_len = max(dfNews[col].astype(str).str.len().max(), len(col) + 2)
            worksheet.set_column(i+1, i+1,column_len)    

    print('Arquivo ', file_name, 'gerado com sucesso!')
