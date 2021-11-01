from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors import SessionPasswordNeededError
import os, sys
import configparser
import csv
import time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from datetime import date
import traceback
from datetime import datetime
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
import datetime
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
cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phones = [i.split(".")[0] for i in glob.glob("*.session")]
    print("=================================")
    print(f"Bất kỳ số điện thoại tùy chỉnh nào khác")
    for _index, i in enumerate(phones):
        print(f"{gr}{_index}. {i} ")
    try:
        index_name = int(input(f"{re}Nhập : "))
        phone = phones[index_name]
    except:
        phone = input(f"{re} Số điện thoại có mã quốc gia : ")
        
    print("Số điện thoại đã chọn là : ",phone)
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] Chạy python3 setup.py trước!!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)

    os.system('clear')
    #banner()
    client.sign_in(phone)
    try:
        client.sign_in(code=input('Nhập code: '))
    except SessionPasswordNeededError:
        client.sign_in(password=getpass.getpass())
try:
    os.system('clear')
except:
    pass
try:
    os.system("cls")
except:
    pass
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Chọn một nhóm để cạo thành viên :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Nhập một số : "+re)
target_group=groups[int(g_index)]
 
print(gr+'[+] Tìm nạp thành viên...')
time.sleep(1)
all_participants = []
all_participants = client.get_participants(target_group, aggressive=True)
 
print(gr+'[+] Lưu trong tệp...')
time.sleep(1)
with open("members.csv","w",encoding='UTF-8') as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n")
    writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
    seens = ['1 ngày', "2 ngày","7 ngày", "15 ngày"]
    for _index, i in enumerate(seens):
        print(f"{gr}{_index}. {i} ")
    try:
        index_name = int(input(f"{re}Nhập : "))
        seen = int(seens[index_name].split(" ")[0])
        print("Chọn {}".format(seen))
    except:
        seen = 0
        print(re+"Đã chọn tất cả người dùng ")
    for user in all_participants:
        try:
            if seen != 0:
                lastDate=user.status.was_online
                datename = lastDate.day
                end_date = datetime.datetime.now()
                start_date = end_date - datetime.timedelta(days=datename)
                difference_in_days = abs((end_date - start_date).days)
                if difference_in_days > seen:
                    continue
        except Exception as e:
            #print(e)
            continue
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        writer.writerow([username,user.id,user.access_hash,name,target_group.title, target_group.id])      
print(gr+'[+] Thành viên đã được cạo thành công. Đăng ký kênh Youtube CodingBeast để thêm thành viên')
