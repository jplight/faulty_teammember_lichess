import requests
import json
import datetime
from os import sys
from configparser import ConfigParser
import re 

id_team = ''

if len(re.findall("s.py$", sys.argv[-1])) == 0:
    id_team = sys.argv[-1]
else: 
    parser = ConfigParser()
    parser.read("parameter.ini")
    configObject = parser["TEAM-CONFIG"]
    id_team = configObject["TeamID"]  


if len(id_team) == 0:
    id_team = input("Team:")


url = "https://lichess.org/api/team/" + id_team + "/users"
param = dict()
resp = requests.get(url=url,params=param)
list_resp = resp.text.splitlines()
data = list(map(lambda x: json.loads(x), list_resp))

fault_users = []
for i in data:
    is_faulti = i.get("tosViolation")
    if is_faulti:
        user = i.get("username")
        fault_users.append(user)

now = datetime.datetime.today()
date = now.strftime('%d.%m.%Y')
datei = open('blacklist.txt','a')
datei.write("\n\nIn the Team " + id_team + ", found at: " + date)
for i in fault_users:
    print(i)
    datei.write("\n" + i)
