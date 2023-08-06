import requests
from typing import List
from zcc_utils.json_tools import json_tools


class HQ2:
    def __init__(self):
        self.Today:List[HQ2Item]=[]
class HQ2Item:
    def __init__(self):
        self.E7=None
        self.E8=None
        self.E9=None
        self.E10=None
        self.E11=None
        self.E12=None
        self.E13=None
        self.V1=None

response = requests.get("https://www.2hq.com.7xq.com/data/GamesDataArray.json")
# print(response.text)
# obj = json.loads(response.text)
# res:HQ2 = dict_to_object(obj)
res:HQ2 = json_tools.json_to_object(response.text)
print(res.Today[0].E7)