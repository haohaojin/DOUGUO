import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from random import randint
import csv
import datetime
import time
import socket
import pymysql

socket.setdefaulttimeout(600)
start_time = time.time()
headers = (
    'User-Agent',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')


# web scraping page 121

def getBookmark(url):
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.find_all("span", {"id": "collectsnum"})  # .parent.previous_sibling.get_text()
        return title[0].getText()
    except AttributeError as e:
        return None


def getVisit(url):
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.find_all("span", {"id": "collectsnum"})[0].previous_sibling.previous_sibling.getText()
        return title
    except AttributeError as e:
        return None


def getRecipe(user, url):
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        h3list = bsObj.find_all("h3")
        #print(len(h3list))
        for recipe in h3list:
            # if "圣诞" in recipe.getText() and "糖霜" in recipe.getText():
            # year = bsObj.find("span", {"class": "yearnum dblok"}).getText()[0:4]
            parent_node = recipe.parent.parent.parent.parent.children
            parent_list = []
            for chi in parent_node:
                parent_list.append(chi)
            # print(parent_list)
            year = bsObj.find_all("span", {"class": "yearnum dblok"})
            recipe_pos = parent_list.index(recipe.parent.parent.parent)
            # print('recipe_pos:' + str(recipe_pos))
            # print(year)
            for i in range(0, len(year)):
                # print(parent_list.index(year[len(year)-1-i].parent))
                if parent_list.index(year[len(year) - 1 - i].parent) < recipe_pos:
                    year_final = year[len(year) - 1 - i].getText()[0:4]
                    # print(year_final)
                    break
            # print(year[0].find_all_next().index(recipe))
            # test = year.previous_sibling.find("span", {"class": "yearnum dblok"})
            # print(test)
            month_temp = recipe.parent.parent.parent.find("span", {"class": "dblok pts"}).getText()
            if len(month_temp) == 3:
                month = month_temp[0:2]
            else:
                month = "0" + month_temp[0]
            day = month_temp = recipe.parent.parent.parent.find("span", {"class": "tdate"}).getText()
            recipe_url = recipe.find("a").attrs['href']
            created_date = datetime.date(int(year_final), int(month), int(day))
            diff = today - created_date
            visited = getVisit(recipe_url)
            bookmarked = getBookmark(recipe_url)
            name = recipe.getText()
            link = recipe.find("a").attrs['href']
            print(user + "|" + today.strftime('%Y/%m/%d') + "|" + created_date.strftime(
                '%Y/%m/%d') + "|" + visited + "|" + bookmarked + "|" + name + "|" + link)
            writer.writerow((user, today.strftime('%Y/%m/%d'), created_date.strftime('%Y/%m/%d'), visited,bookmarked, name, link))

            user_sql = '\"' + user + '\"'
            date = today.strftime('%Y-%m-%d')
            date_sql = '\"' + date + '\"'
            created_date = created_date.strftime('%Y-%m-%d')
            created_date_sql = '\"' + created_date + '\"'
            name_sql = '\"' + name + '\"'
            link_sql = '\"' + link + '\"'

            sql = "REPLACE INTO `recipe` (`user`, `date`, `created_date`, `visited`, `bookmarked`, `name`, `link`) VALUES (" + user_sql + ", " + date_sql + ", " + created_date_sql + ", " + str(
                    visited) + ", " + str(bookmarked) + ", " + name_sql + ", " + link_sql + ")"
            #print(sql)
            cur.execute(sql)
            cur.connection.commit()

            # print(visited)
            # print(getVisit(recipe_url))
            # print(bookmarked)
            # print(getBookmark(recipe.find("a").attrs['href']))
            # print(name)
            # print(recipe.getText())
            # print(link)
            # print(recipe.find("a").attrs['href'])

        title = bsObj.find_all(lambda tag: tag.getText() == '下一页')
        if (len(title) != 0):
            # print(title)
            newpage = title[0].find("a").attrs['href']
            # print(newpage)
            newpage_decoded = newpage.replace("圣诞 糖霜", "%E5%9C%A3%E8%AF%9E%20%E7%B3%96%E9%9C%9C")
            # print(newpage_decoded)
            # time.sleep(randint(5, 9))
            getRecipe(user, newpage_decoded)
    except AttributeError as e:
        return None

searchList = {'Breadmum': 'http://www.douguo.com/u/u30362766298239/recipe',
              }

today = datetime.date.today()

conn = pymysql.connect(host='127.0.0.1',  # unix_socket='/tmp/mysql.sock',
                       user='read', passwd='read', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE breadmum_recipe")

for i in searchList:
    print(i, searchList[i])
    with open("C:/Users/hao.jin/Desktop/Python/" + i + '-' + str(today) + ".csv", 'w', newline='',
              encoding='UTF-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(('User', 'Added Date', 'Created Date', 'Visited', 'Bookmarked', 'Name', 'Link'))
        getRecipe(i, searchList[i])
        csvFile.close()
    print("--- %s seconds ---" % (time.time() - start_time))

cur.close()
conn.close()
print("--- %s seconds ---" % (time.time() - start_time))
