import os
import requests, threading
import  json
import time

API_ENDPOINT = 'https://discord.com/api/v9'
CLIENT_ID = '1088101727170998273'
CLIENT_SECRET = "4zbiSb--zDgZmEBmLXjGbAxQOQYk8uHn"
REDIRECT_URI = 'https://maybe-oauth2.cyberhouse.repl.co'
tkn = "MTA4ODEwMTcyNzE3MDk5ODI3Mw.G3oQrC.WWJAL2daHfXeKGIpWGm8liH2yi0uNOWW7ey_C0"

def add_to_guild(access_token, userID , guild_Id ):
    while True:
        url = f"{API_ENDPOINT}/guilds/{guild_Id}/members/{userID}"

        botToken = tkn
        data = {
        "access_token" : access_token,
    }
        headers = {
        "Authorization" : f"Bot {botToken}",
        'Content-Type': 'application/json'

    }
        response = requests.put(url=url, headers=headers, json=data)
        if response.status_code in (200, 201, 204):
          print(f"[INFO]: successfully added {userID} to {guild_Id}")
          break
        else:
           print(response.status_code)
           print(response.text)
           if 'retry_after' in response.text:
               sleepxd = int(response.json()['retry_after']) + 0.5
               time.sleep(sleepxd)
               continue


count = 0 
def get_new_token(refresh):
  jsonxd = None
  global count
  count += 1
  while True:
    print(count, "Refreshing token:", refresh)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'grant_type': 'refresh_token',
      'refresh_token': refresh
    }
    r = requests.post(f"{API_ENDPOINT}/oauth2/token", data=data, headers=headers)
    print(r.status_code)
    print(r.text)
    print(r.json())
    if r.status_code in (200, 201, 204):
      jsonxd = r.json()
      break
    elif r.status_code == 429:
      continue
    else:
      break
  return jsonxd



f = open('database.txt', 'r').readlines()
f2 = open('refreshed.txt', 'a')

def refresher(line):
  # print(line)
  line = line.split(':')
  try:
    refresh = line[2]
    print(refresh)
    r = get_new_token(refresh)
    id = line[0]
    new_refresh = r['refresh_token']
    access = r['access_token']
    f2.write(f"{id}:{access}:{new_refresh}\n")
    # add_to_guild(access_token=access, userID=id, guild_Id="1058692430276333619")
    # add_to_guild(access_token=access, userID=id, guild_Id="952495772073619466")
  except:
    pass

for line in f:
  if "\n" in line:
    line = line.replace("\n", "")

  # threading.Thread(target=refresher, args=(line,)).start()
  # time.sleep(1)
  refresher(line)