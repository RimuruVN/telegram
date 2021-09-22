from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import configparser
import os
import sys
import csv
import traceback
import time
import random
from time import sleep
import getpass
from telethon.errors import SessionPasswordNeededError
import sys
import glob
re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""{gr}
  ____          _ _             ____                 _   
 / ___|___   __| (_)_ __   __ _| __ )  ___  __ _ ___| |_ 
| |   / _ \ / _` | | '_ \ / _` |  _ \ / _ \/ _` / __| __|
| |__| (_) | (_| | | | | | (_| | |_) |  __/ (_| \__ \ |_ 
 \____\___/ \__,_|_|_| |_|\__, |____/ \___|\__,_|___/\__|
                          |___/                        

              Version : 1.01
 {re}Subscribe CodingBeast on Youtube.
   {cy}www.youtube.com/c/CodingBeast
        """)
banner()
print (cy+"version : 1.01")
print (cy+"Make sure you Subscribed CodingBeast On Youtube")
print (cy+"www.youtube.com/codingbeast")

print (re+"NOTE :")
print ("1. Telegram only allow to add 200 members in group by one user.")
print ("2. You can Use multiple Telegram accounts for add more members.")
print ("3. Add only 50 members in group each time otherwise you will get flood error.")
print ("4. Then wait for 15-30 miniute then add members again.")
print ("5. Make sure you enable Add User Permission in your group")

cpass = configparser.RawConfigParser()
cpass.read('config.data')
phones = [i.split(".")[0] for i in glob.glob("*.session")]
print("=================================")
print(f"any other number of custom phone")
for _index, i in enumerate(phones):
    print(f"{gr}{_index}. {i} ")
try:
    index_name = int(input(re+"Enter : "))
    phone = phones[index_name]
except:
    phone = input(re+" phone with country code : ")
    
print(cy+"selected phone is : ",phone)

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = phone
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    #banner()
    print(re+"[!] run python setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)

    os.system('clear')
    #banner()
    client.sign_in(phone)
    try:
        client.sign_in(code=input('Enter code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=getpass.getpass())
  
users = []
with open(r"members.csv", encoding='UTF-8') as f:  #Enter your file name
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        #print(row)
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup == True:
            groups.append(chat)
    except:
        continue

print(gr+'Choose a group to add members:'+cy)
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input(gr+"Enter a Number: "+re)
target_group = groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

mode = 1 #int(input(gr+"Enter 1 to add by username or 2 to add by ID: "+cy))

n = 0

for user in users:
    if os.path.exists("back.log"):
             with open("back.log", "r") as read:
                   ids = [i.strip("\n") for i in read.readlines()]
             if user['username'] in ids:
                   print("user already invited skiped..........")
                   continue
    n += 1
    if n % 80 == 0:
        sleep(60)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")

        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
        print("Waiting for 60-180 Seconds...")
        with open("back.log","a") as rp:
             rp.write(user['username'] +"\n")
        time.sleep(random.randrange(0, 5))
    except PeerFloodError:
        SLEEP_TIME_2 = 60
        print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        print("Waiting {} seconds".format(SLEEP_TIME_2))
        time.sleep(SLEEP_TIME_2)
        with open("back.log","a") as rp:
             rp.write(user['username'] +"\n")
        client.disconnect()
        sys.exit()
    except UserPrivacyRestrictedError:
        print("The user's privacy settings do not allow you to do this. Skipping.")
        print("Waiting for 5 Seconds...")
        time.sleep(random.randrange(0, 5))
        with open("back.log","a") as rp:
             rp.write(user['username'] +"\n")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        with open("back.log","a") as rp:
             rp.write(user['username'] +"\n")
        continue
