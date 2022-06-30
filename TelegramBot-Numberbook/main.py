import requests
import json
import time
from threading import Thread

url_telegram = 'https://api.telegram.org/bot{API_TOKEN}'
ID = str()
first_name = str()
users = int()


def UnicodeDecoder(text):
    Result = text.replace("\\u0627", "ا").replace("\\u0628", "ب").replace("\\u062a", "ت").replace("\\062b","ث").replace("\\u062c", "ج").replace("\\u062d", "ح").replace("\\u062e", "خ").replace("\\u062f", "د").replace("\\u0630","ذ").replace("\\u0631", "ر").replace("\\u0632", "ز").replace("\\u0633", "س").replace("\\u0634", "ش").replace("\\u0635","ص").replace("\\u0636", "ض").replace("\\u0637", "ط").replace("\\u0638", "ظ").replace("\\u0639", "ع").replace("\\u063a","غ").replace("\\u0641", "ف").replace("\\u0642", "ق").replace("\\u0643", "ك").replace("\\u0644", "ل").replace("\\u0645","م").replace("\\u0646", "ن").replace("\\u0647", "ه").replace("\\ufeea", "ﻪ").replace("\\u0647", "ﻫ").replace("\\ufeeb","ﻫ").replace("\\u0648", "و").replace("\\u064a", "ي").replace("\\u0622", "آ").replace("\\ufe81", "ﺁ").replace("\\u0629","ة").replace("\\u0649", "ى").replace("\\ufeed", "ﻯ").replace("\\ufef0", "ﻰ").replace("\\ufef3", "ﻳ").replace("\\ufef2","ﻲ").replace("\\u0640", "ـ").replace("\\ufed9", "ﻙ").replace("\\ufe8e", "ﺎ").replace("\\u060c", "،").replace("\\ufd3e","﴾").replace("\\ufd3f", "﴿").replace("\\u06d4", "۔‎").replace("\\u061b", "؛").replace("\\ufdf0", "ﷰ").replace("\\ufdf1","ﷱ‎").replace("\\ufdf6", "ﷶ").replace("\\ufdf9".strip(), "ﷹ").replace("\\u0660", "۰").replace("\\u0661", "۱").replace("\\u0662", "۲").replace("\\u0663", "۳").replace("\\u0664", "٤").replace("\\u0665", "٥").replace("\\u0666","٦").replace("\\u0667", "٧").replace("\\u0668", "۸").replace("\\u0669", "۹").replace("\\u061f", "؟").replace("\\u0623","أ").replace("\\u0624", "ؤ").replace("\\u0626", "ئ").replace("\\u0621", "ء").replace("\\u06af", "گ").replace("\\u06a4","ڤ").replace("\\u0698", "ژ").replace("\\u003e", ">").replace("\\u003c", "<").replace("\\u00a3", "£").replace("\\u20ac","€").replace("\\u064e", "َ").replace("\\u0652", "ْ").replace("\\u064f", "ُ").replace("\\u0650", "ِ").replace('\\u0026','&').replace('\\u003d','=').replace("٠","0").replace("۱","1").replace("۲","2").replace("۳","3").replace("٤","4").replace("٥","5").replace("٦","6").replace("٧","7").replace("٨","8").replace("٩","9")
    return Result

def ChatUpdater():
    global ID
    global first_name
    try:
        msg = ''
        id = ''
        r = requests.get(url_telegram + "/getupdates").text
        rs = json.loads(r)
        for res in rs['result']:
            if "my_chat_member" in res:
                pass
            else:
                msg = res['message']['text']
                id = res['message']['from']['id']
                first_name = res['message']['from']['first_name']
        return str(id) + "|" + str(msg)
    except KeyError:
        pass


def NumberBook(phone_number):
    try:

        res = requests.get(f"http://146.148.112.105/caller/index.php/UserManagement/search_number?number={phone_number}&country_code=SA").json()
        if "No recourd found" not in res:
            for i in res['result']:
                return i['name']
        else: return "Not Found"
    except: return "Not Found"

def SendMessage(msg):
    PostData = {
        'chat_id': ID , 'text': msg
    }
    requests.post(url_telegram+"/sendMessage" , data=PostData)


def MainMethod():
    global users
    global ID
    old_id = ''
    old_msg = ''
    try:
       while True:
           response = ChatUpdater()
           ID = response.split("|")[0]
           message = response.split("|")[1]
           message = UnicodeDecoder(message)
           if old_msg != message:
               old_msg = message
               old_id = ID
               users += 1
               print(f"Users [ {users} ]", end="\r", flush=True)
               if message.upper() == "/START" or message.upper() == "START" or message.upper() == "HELP" or message.upper() == "/HELP":
                   SendMessage(f"""اهلاً بك {first_name} في دليل الهاتف☎️

فضلاً ارسل رقم الجوال بدون مفتاح الدولة 
مثال :  
05x xxx xxxx

ملاحظة❗️: البوت حاليًا مايشتغل الا على ارقام سعودية فقط 🇸🇦

مستقبلاً بيكون فيه تطوير 🔹
""")
               elif message.isdigit():
                 if len(message) != 10 :
                     SendMessage("الرقم خاطئ !!")
                     continue
                 if message[0] == "0":
                     message = message[1:]
                 SendMessage("Wait .. ")
                 MESSAGE = f"""- الرقم 📱:  0{message} 
- الاسم 👤 : {NumberBook(message)}
الدولة 🌍 : المملكة العربية السعودية🇸🇦

شكرًا لاستخدام البوت 🙏
فضلاً انشر البوت عشان يستفيد غيرك📲

اذا حاب تنشر البوت 
اضغط /infobot
                 """
                 SendMessage(MESSAGE)
               elif message.lower() == "/infobot":
                   SendMessage("""بوت استخراج الاسم من الرقم ☎️
Link : """) #  your channel link

           else:
               if old_id != ID:
                   old_id = ''
                   continue
    except Exception as w:pass
    time.sleep(2.5)


Thread(target=MainMethod()).start()
