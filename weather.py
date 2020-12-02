import re
import pymysql
import requests
from bs4 import BeautifulSoup

class SearchWeather():
    def __init__(self):
        self.HEADERS ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ''(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
        self.CONNECTION = pymysql.connect(host='localhost',user='root',password='123456',db='city',charset='utf8',cursorclass=pymysql.cursors.DictCursor)

    def getcityCode(self,cityName):
        SQL = "SELECT cityCode FROM cityWeather WHERE cityName='{}'".format(cityName)
        try:
            with self.CONNECTION.cursor() as cursor:
                cursor.execute(SQL)
                self.CONNECTION.commit()
                result = cursor.fetchone()
                print('城市代码：',result['cityCode'])
                return result['cityCode']
                
        except Exception as e:
            print(repr(e))                  
            

    def getWeather(self,cityCode,cityname):
        url = 'http://www.weather.com.cn/weather/{}.shtml'.format(cityCode)
        html = requests.get(url,headers = self.HEADERS)
        html.encoding='utf-8'
        soup=BeautifulSoup(html.text,'lxml')
        weather = "日期      天气    【温度】    风向风力\n"
        i = 1
        for item in soup.find("div", {'id': "7d"}).find('ul').find_all('li'):
            date,detail = item.find('h1').string, item.find_all('p')
            title = detail[0].string
            templow = detail[1].find("i").string
            temphigh = detail[1].find('span').string if detail[1].find('span')  else ''
            wind,direction = detail[2].find('span')['title'], detail[2].find('i').string
            if temphigh=='':
                weather += '你好，【{1}】今天白天：【{2}】，温度：【{3}】，{4}：【{5}】\n'.format(cityname,title,templow,wind,direction)
            else:
                if i < 7:
                    weather += (date + title + "【" + templow +  "~"+temphigh +'°C】' + wind + direction + "\n")
                else:
                    weather += (date + title + "【" + templow + "~" + temphigh + '°C】' + wind + direction)
            i += 1
        return weather
    

    
    def getWeather15(self,cityCode,cityname):
        url = 'http://www.weather.com.cn/weather15d/{}.shtml'.format(cityCode)
        html = requests.get(url,headers = self.HEADERS)
        html.encoding='utf-8'
        soup=BeautifulSoup(html.text,'lxml')
        weather = ""
        for item in soup.find("div", {'id': "15d"}).find('ul').find_all('li'):
            date,detail = item.find('span').string, item.find_all('span')
            if len(date)==6:
                date = date[3:5] + "（" + date[0:2] + "）"
            else:
                date = date[3:6] + "（" + date[0:2] + "）"
            title = detail[1].string
            templow = detail[2].get_text()
            temphigh = detail[2].find('em').string if detail[2].find('em')  else ''
            wind,direction = detail[3].string, detail[4].string
            weather += (date + title + "【" + templow[-3:-1] +  "~"+temphigh +"】" + wind + direction + "\n")
        return weather

    def main(self,city):
        cityCode = self.getcityCode(city)
        detail = self.getWeather(cityCode,city)
        detail15 = self.getWeather15(cityCode,city)
        print(detail)
        print(detail15)

if __name__ == "__main__":
    while 1==1:
        weather = SearchWeather()
        weather.main(city=input('请输入城市名称：'))
            
