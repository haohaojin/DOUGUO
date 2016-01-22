# http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe
import requests
res = requests.post(u'http://m.douguo.com/activity/recipecollect/ajaxGetMoreRecipe', data={"offset":10,"pid":419})
print(res.text)