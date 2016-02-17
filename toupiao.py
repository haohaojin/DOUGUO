# http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe
import requests

size = 10
position = 0

while size == 10:
    # http://m.douguo.com/
    # 419 金龙鱼
    # http://m.douguo.com/ajax/dopull/209546/7200/26/
    # http://m.douguo.com/ajax/dopull/209248/7200/26/
    # 428 六月鲜
    # http://m.douguo.com/ajax/dopull/210827/7200/26/
    # 430 均衡年夜饭
    # http://m.douguo.com/ajax/dopull/212391/7200/26/

    # Expired
    # 417 维达
    # /activity/newtry/trylist/'+id+'/'+offset
    res = requests.post(u'http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe', data={"offset":position,"pid":434}) #173 is the last one
    string = res.json()
    # print(string)

    # print("status: " + string["status"])
    # print(len(string["data"]))

    iter = range(0,len(string["data"]))
    for i in iter:
        recipe = string["data"][i]
        data = recipe["recipe"]
        user = data["user_info"]
        if user["nickname"] == 'breadmum':
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
