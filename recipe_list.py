import urllib.request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv
import datetime
import time
import socket
import pymysql
import re

socket.setdefaulttimeout(600)
start_time = time.time()
headers = (
    'User-Agent',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')


# web scraping page 137


def getAttributes(url):
    result = []
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        fans_list = bsObj.find_all("a", {"href": re.compile(r'.fans')})
        fans = fans_list[0].getText()
        friends_list = bsObj.find_all("a", {"href": re.compile(r'.friends')})
        friends = friends_list[0].getText()
        jifen_list = bsObj.find_all("a", {"href": "/jifen/product/lists"})
        jifen = jifen_list[0].getText().strip()
        daren_flag = '#'
        daren_title = '#'
        daren_flag_list = bsObj.find_all("a", {"href": "/user/prodesc"})
        if len(daren_flag_list) > 0:
            daren_flag = 'C'
            daren_title_list = bsObj.find_all("span", {"class": "fss inblok fcc"})
            daren_title = daren_title_list[0].getText()
        result.append(fans)
        result.append(friends)
        result.append(jifen)
        result.append(daren_flag)
        result.append(daren_title)
        # print(result)
        return result
    except AttributeError as e:
        return None

def getRecipeDetail(url):
    recipeDetail = []
    try:
        html = urllib.request.urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        bookmark = bsObj.find_all("span", {"id": "collectsnum"})  # .parent.previous_sibling.get_text()
        recipeDetail.append(bookmark[0].getText())
        visit = title = bsObj.find_all("span", {"id": "collectsnum"})[0].previous_sibling.previous_sibling.getText()
        recipeDetail.append(visit)
        return recipeDetail
    except AttributeError as e:
        return None

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
        # print(len(h3list))
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

            month_temp = recipe.parent.parent.parent.find("span", {"class": "dblok pts"}).getText()
            if len(month_temp) == 3:
                month = month_temp[0:2]
            else:
                month = "0" + month_temp[0]
            day = month_temp = recipe.parent.parent.parent.find("span", {"class": "tdate"}).getText()
            recipe_url = recipe.find("a").attrs['href']
            created_date = datetime.date(int(year_final), int(month), int(day))
            diff = today - created_date
            recipeDetail = getRecipeDetail(recipe_url)
            visited = recipeDetail[1]
            bookmarked = recipeDetail[0]
            name = recipe.getText().replace('"', '""')
            link = recipe.find("a").attrs['href']
            print(user + "|" + today.strftime('%Y/%m/%d') + "|" + created_date.strftime(
                '%Y/%m/%d') + "|" + visited + "|" + bookmarked + "|" + name + "|" + link)
            # writer.writerow((user, today.strftime('%Y/%m/%d'), created_date.strftime('%Y/%m/%d'), visited, bookmarked,
            #                  name, link))
            user_sql = '\"' + user + '\"'
            date = today.strftime('%Y-%m-%d')
            date_sql = '\"' + date + '\"'
            created_date = created_date.strftime('%Y-%m-%d')
            created_date_sql = '\"' + created_date + '\"'
            name_sql = '\"' + name + '\"'
            link_sql = '\"' + link + '\"'
            fans = attributes[0]
            friends = attributes[1]
            jifen = attributes[2]
            daren_flag = '\"' + attributes[3] + '\"'
            daren_title = '\"' + attributes[4] + '\"'

            sql = "REPLACE INTO `recipe` (`user`, `date`, `created_date`, `visited`, `bookmarked`, `name`, `link`,`fans`,`friends`,`jifen`,`daren_flag`,`daren_title`) VALUES (" + user_sql + ", " + date_sql + ", " + created_date_sql + ", " + str(
                    visited) + ", " + str(
                bookmarked) + ", " + name_sql + ", " + link_sql + ", " + fans + ", " + friends + ", " + jifen + ", " + daren_flag + ", " + daren_title + ")"
            # print(sql)
            cur.execute(sql)
            cur.connection.commit()

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


searchList = {#'Breadmum': 'http://www.douguo.com/u/u30362766298239/recipe',  #
                  #'胡小may': 'http://www.douguo.com/u/u55783496151049/recipe',  #
                  #'美国厨娘': 'http://www.douguo.com/u/u35246655713154/recipe',
                  #'小米554': 'http://www.douguo.com/u/u21252191430097/recipe',  #
                  #'爱生活的馋猫': 'http://www.douguo.com/u/u20468009171777/recipe',  #
                  #'夏夏夏洛特的烤箱': 'http://www.douguo.com/u/u42706554805034/recipe',  #
                  #'牛一的小饭桌和大饭': 'http://www.douguo.com/u/u0722865253319/recipe',
                  #'恬萝姑娘': 'http://www.douguo.com/u/u07131690939285/recipe',
                  #'Lola_ohlala': 'http://www.douguo.com/u/u0653952018640/recipe',
                  #'默默扒猪皮': 'http://www.douguo.com/u/u96695973600527/recipe',
                  #'兔美酱': 'http://www.douguo.com/u/u90220649629766/recipe',
                  #'亦梦亦乐Angel': 'http://www.douguo.com/u/u83785502684561/recipe',
                  #'我家厨房香喷喷': 'http://www.douguo.com/u/u79475897300517/recipe',
                  #'饭小小': 'http://www.douguo.com/u/u70173438368099/recipe',
                  #'纷纷712': 'http://www.douguo.com/u/u65346612779426/recipe',
                  #'肥小菇': 'http://www.douguo.com/u/u6376841712552/recipe',
                  #'Tella陈珊珊': 'http://www.douguo.com/u/u63256997684102/recipe',
                  #'美美家的厨房': 'http://www.douguo.com/u/u57369189548912/recipe',
                  #'臭美园妈': 'http://www.douguo.com/u/u5536282897462/recipe',
                  #'拾光机': 'http://www.douguo.com/u/u54285202635742/recipe',
                  #'糖小饼': 'http://www.douguo.com/u/u40952060753467/recipe',
                  #'Snaker的音樂厨房': 'http://www.douguo.com/u/u23231065/recipe',
                  #'君之': 'http://www.douguo.com/u/u08363793/recipe',
                  #'lovestory9': 'http://www.douguo.com/u/u06633444602482/recipe',
                  #'贝尔烘焙': 'http://www.douguo.com/u/u9703241974907/recipe',
                  #'孟尤尤': 'http://www.douguo.com/u/u70689723621271/recipe',
                  #'米多小鱼': 'http://www.douguo.com/u/u62023329732653/recipe',
                  #'牛妈厨房': 'http://www.douguo.com/u/u05300914/recipe',
                  }

today = datetime.date.today()

conn = pymysql.connect(host='127.0.0.1',  # unix_socket='/tmp/mysql.sock',
                       user='read', passwd='read', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE breadmum_recipe")

for i in searchList:
    print(i, searchList[i])
    attributes = getAttributes(searchList[i].replace('/recipe', '.html'))
    # print(attributes)
    # with open("C:/Users/hao.jin/Desktop/Python/" + i + '-' + str(today) + ".csv", 'w', newline='',
    #           encoding='UTF-8') as csvFile:
        # writer = csv.writer(csvFile)
        # writer.writerow(('User', 'Added Date', 'Created Date', 'Visited', 'Bookmarked', 'Name', 'Link'))
    getRecipe(i, searchList[i])
        # csvFile.close()
    print("--- %s seconds ---" % (time.time() - start_time))

cur.close()
conn.close()
print("--- %s seconds ---" % (time.time() - start_time))
