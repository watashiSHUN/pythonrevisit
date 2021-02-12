import requests
import json

response = requests.get("https://www.randomlists.com/data/words.json")
json_dict = json.loads(response.text)
# print(type(json_dict['data']))
words = json_dict['data'] # exported
