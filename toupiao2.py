# http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe
import requests

res = requests.post(u'http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe', data={"offset":188,"pid":419}) #173 is the last one
string = res.json()

print("status: " + string["status"])
print(len(string["data"]))


