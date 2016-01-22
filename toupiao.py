# http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe
import requests

size = 10
position = 0

while size == 10:
    res = requests.post(u'http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe', data={"offset":position,"pid":419}) #173 is the last one
    string = res.json()

    print("status: " + string["status"])
    print(len(string["data"]))
    iter = range(0,len(string["data"]))
    for i in iter:
        recipe = string["data"][i]
        data = recipe["recipe"]
        user = data["user_info"]
        print("nickname: "+ user["nickname"])
        print("name: " + str(data["name"]))
        print("activity id: " + recipe["id"])
        print("recipe id: " + str(data["id"]))
        print("is_pull: " + str(recipe["is_pull"]))
        print("pull_num: " + str(recipe["pull_num"]))
        print("like_num: " + str(data["like_num"]))
        print("view_num: " + str(data["view_num"]))
        print("dish_num: " + str(data["dish_num"]))
        print("image: " + str(data["image"]))
        print("headicon: " + user["headicon"])
        print()
    size = len(string["data"])
    position += 10
