from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import pandas as pd
import re 
import csv
import openpyxl
import xlsxwriter
import time
newsList=[]
contentsList=[]
titleNews_onlytext=[]
contentNews_onlytext=[]
newsList_formatted=[]
contentsList_formatted=[]
linkstoNews_list=[]


def patternRegex(value):
    pattern=r'^(?!").*$'
    newValue=re.compile(pattern,value)
    return newValue

def innerHTML(element):
    """Returns the inner HTML of an element as a UTF-8 encoded"""
    return element.encode_contents()

#csvFileName = 'Últimas_Notícias.csv'
#regexMovieYear = re.compile('(\d{4})')
#regexUserRating = re.compile('\ ((\d{1,3})((\,|\.)\d{1,3})*)')

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
        #print(i)
        titleNews_onlytext.append(innerHTML(i))
    for i in titleNews_onlytext:
            newsList.append(i.decode("utf-8", "strict"))

    #print(newsList)

    linkstoNews = html.find_all("a", {"class": "feed-post-link gui-color-primary gui-color-hover"})
    for i in linkstoNews:
        #print(i)
        linkstoNews_list.append(i['href'])
    

    

    contentNews = html.find_all("div", {"class": "feed-post-body-resumo"})
    for r in contentNews:
        contentNews_onlytext.append(innerHTML(r))
    for r in contentNews_onlytext:
        contentsList.append(r.decode("utf-8", "strict"))
    
    data = {'News': newsList, 'Contents':contentsList, 'Links': linkstoNews_list}
    dfNews= pd.DataFrame(data)
    


  
    # with open(csvFileName, 'w') as csvfile:
    #     fileWriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    #     fileWriter.writerow(['News','Abstract']) #HEADER 

    #     for j,q in zip(newsList,contentsList):        
    #         fileWriter.writerow([j,q]) #CONTENT

            
    #     print('Arquivo ', csvFileName, 'gerado com sucesso!')

    print(dfNews)

    file_name='Ultimas_Noticias.xlsx'

    
    dfNews.to_excel(file_name,sheet_name='Sheet1')
   
    print(dfNews)

    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
    
        dfNews.to_excel(excel_writer=writer)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

    # dynamically set column width
        for i, col in enumerate(dfNews.columns):
            print(i,col)
            column_len = max(dfNews[col].astype(str).str.len().max(), len(col) + 2)
            print(len(col) + 2)
            worksheet.set_column(i+1, i+1,column_len)

    #dfNews.to_excel(excel_writer=writer, sheet_name='Sheet1')

    

    print('Arquivo ', file_name, 'gerado com sucesso!')