#!/usr/bin/python

from telegram.ext import CommandHandler, Updater, ConversationHandler, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from re import search
from os import system
from requests import post
from time import sleep
from threading import Thread
import sqlite3
import Api


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
    if s == 0:
        c.execute(f''' INSERT INTO Users (ChatID, Name, VipTest, LTarget, Subset, License, BanMood) VALUES ("{Chat_id}", "{name}", "{viptest}", "{targets}", "{subset}", "{license}", "{banmood}")''')
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

def start(update, context):
    main_InsertToDB(update.message.chat_id, update.message.from_user.name, 0, 0, 0, 0, 0)
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
            update.message.reply_text('سلام\nبه ربات اس ام اس بمبر خوش آمدید.\n——————————————\nبرای مشاهده دستورات /help را ارسال کنید.', reply_markup=ReplyKeyboardRemove(['لغو']))
    elif bmm :
        update.message.reply_text('شما از ربات بن شده اید.')



def help(update, context):
    CheckBan(update.message.chat_id)
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
        else:
            if update.message.chat_id != Admin_Chatid:
            # update.message.reply_text('لیست دستورات:\n——————————————\nاستارت کردن ربات\n/start\n——————————————\n/FreeMood\n❇️ روشن کردن اس ام اس بمبر با یک سرور\nمحدودیت ها:\n🔻سرعت کم\n🔻اسپم با یک سرور\n🔻محدودیت ارسال پیام\n——————————————\n/VipMood\n🔥فعال کردن اسپمر اس ام اس با 26 سرور مختلف\nمزیت ها:\n🔻اسپم با 26 سرور و شماره مختلف\n🔻سرعت بالا در ارسال پیامک\n🔻بدون محدودیت ارسال پیامک\n——————————————\n/Viptest\n😁تست بخش Vip')
                update.message.reply_text('''لیست دستورات:
——————————————
استارت کردن ربات
/start
——————————————
/info
مشاهده اطلاعات حساب کاربری
——————————————
/FreeMood
❇️ روشن کردن اس ام اس بمبر با یک سرور
محدودیت ها:
🔻سرعت کم
🔻اسپم با یک سرور
🔻محدودیت ارسال پیام
——————————————
/VipMood
🔥فعال کردن اسپمر اس ام اس با 26 سرور مختلف
مزیت ها:
🔻اسپم با 26 سرور و شماره مختلف
🔻سرعت بالا در ارسال پیامک
🔻بدون محدودیت ارسال پیامک
——————————————
/Viptest
😁تست بخش Vip''')
            else:
            # update.message.reply_text('راهنمای ادمین:\n————————————————\n/Sendtoall\nارسال پیام همگانی\n————————————————\n/Forwardtoall\nفوروارد پیام برای همه کاربران\n————————————————\n/SeeUsers\nمشاهده لیست کاربران\n————————————————\n/GetDB\nدانلود دیتابیس')
                update.message.reply_text('''☸️لیست دستورات کاربر:
——————————————
استارت کردن ربات
/start
——————————————
/FreeMood
❇️ روشن کردن اس ام اس بمبر با یک سرور
محدودیت ها:
🔻سرعت کم
🔻اسپم با یک سرور
🔻محدودیت ارسال پیام
——————————————
/VipMood
🔥فعال کردن اسپمر اس ام اس با 26 سرور مختلف
مزیت ها:
🔻اسپم با 26 سرور و شماره مختلف
🔻سرعت بالا در ارسال پیامک
🔻بدون محدودیت ارسال پیامک
——————————————
/Viptest
😁تست بخش Vip
——————————————
☢لیست کامند های ادمین:️
(روی کامند مورد نظر کلیک کنید)
----------------------------
/Sendtoall
ارسال پیام به همه کاربران
----------------------------
/Forwardtoall
فوروارد پیام به همه کاربران
----------------------------
/SeeUsers
مشاهده لیست کاربران
----------------------------
/GetDB
دانلود دیتابیس
----------------------------
/BanSB
بن کردن کاربر از ربات
----------------------------
/UnBanSB
آزاد کردن کاربر در ربات
----------------------------
/UpToLicense
ارتقا کاربر به ویژه
----------------------------
/DownToLicense
تنزل کاربر به عادی''')
    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')
#####################################OneApi####################################################################

oneApi_GetTarget, oneApi_GetCount = range(2)

CKeyboard = [["لغو"]]
global CMarkup
CMarkup = ReplyKeyboardMarkup(CKeyboard, one_time_keyboard=True, resize_keyboard=True)

def OneApi_Start(update, context):
    CheckBan(update.message.chat_id)
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            update.message.reply_text("لطفا شماره هدف را وارد کنید.", reply_markup=CMarkup)

            return oneApi_GetTarget
    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')

        return ConversationHandler.END

def OneApi_GetTarget(update, context):
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text(
            'لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    else:
        global phone
        phone = update.message.text
        InsertTarget(phone, update.message.chat_id)
        update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        return oneApi_GetCount

def OneApi_GetCount(update, context):
    try:
        if int(update.message.text) <= 0 or int(update.message.text) >= 100 :
            update.message.reply_text('لطفا یک عدد بین 0-100 وارد کنید.')
        else:
            global count
            count = int(update.message.text)
            update.message.reply_text('درحال اسپم کردن...')
            while Api.count < count:
                Thread(target=Api.snap, args=[phone]).start()
                Thread(target=Api.snap, args=[phone]).start()
                Thread(target=Api.snap, args=[phone]).start()
                system("killall -HUP tor")
                print('threaded')
                sleep(3)
            Api.count = 0
            update.message.reply_text(f'{count} اس ام اس به شماره {phone} ارسال شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))

            return ConversationHandler.END
    except:
        update.message.text('لطفا یک عدد وارد کنید.')

def Laghv(update, context):
    update.message.reply_text('عملیات لغو شد.\nلطفا برای مشاهده دستورات /help را ارسال کنید.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
    return ConversationHandler.END

oneApi_conv = ConversationHandler(
    entry_points=[CommandHandler('FreeMood', OneApi_Start)],
    states={
        oneApi_GetTarget : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), OneApi_GetTarget)],
        oneApi_GetCount : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), OneApi_GetCount)],
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)

#####################################OneApi####################################################################

#####################################VipMood###################################################################

vip_GetTarget, vip_GetCount = range(2)

def VipMood_Start(update, context):
    CheckBan(update.message.chat_id)
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            CheckLicense(update.message.chat_id)
            if not li:
                update.message.reply_text('''حساب کاربری شما عادی میباشد.
شما میتوانید برای ویژه کردن حساب خود با آیدی @itsid در ارتباط باشید.
یا دستور /subset را ارسال کنید.''')
                return ConversationHandler.END
            else:
                update.message.reply_text('قدر دان اعتمادتون هستیم :)\nلطفا شماره هدفتون رو وارد کنید.',
                                          reply_markup=CMarkup)
                return vip_GetTarget

    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')
        return ConversationHandler.END


def Vip_GetTarget(update, context):
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text('لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    else:
        global phone
        phone = update.message.text
        InsertTarget(phone, update.message.chat_id)
        update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        return vip_GetCount

def Vip_GetCount(update, context):
    try:
        global count
        count = int(update.message.text)
        update.message.reply_text('درحال اسپم کردن با 26 سرور...')
        while Api.count < count:
            Thread(target=Api.snap, args=[phone]).start()
            Thread(target=Api.shad, args=[phone]).start()
            Thread(target=Api.gap, args=[phone]).start()
            Thread(target=Api.tap30, args=[phone]).start()
            Thread(target=Api.emtiaz, args=[phone]).start()
            Thread(target=Api.divar, args=[phone]).start()
            Thread(target=Api.rubika, args=[phone]).start()
            Thread(target=Api.torob, args=[phone]).start()
            system("killall -HUP tor")
            print('threaded')
            sleep(3)
        Api.count = 0
        update.message.reply_text(f'{count} اس ام اس به شماره {phone} ارسال شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
        return ConversationHandler.END
    except:
        update.message.reply_text('لطفا یک عدد وارد کنید.')

vip_conv = ConversationHandler(
    entry_points=[CommandHandler("VipMood", VipMood_Start)],
    states={
        vip_GetTarget : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), Vip_GetTarget)],
        vip_GetCount : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), Vip_GetCount)],
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)

#####################################VipMood###################################################################

#####################################VipTest################################################################

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

def VipTest_Start(update, context):
    CheckBan(update.message.chat_id)
    if str(bmm) == '0':
        if context.bot.get_chat_member(-1001144465509, update.message.chat_id).status == 'left':
            update.message.reply_text('لطفا در کانال @MrSMSBomber عضو شده و مجدد /start را ارسال کنید.')
            return ConversationHandler.END
        else:
            CheckVipTest(update.message.chat_id)
            if not tv:
                update.message.reply_text(
                    'توجه داشته باشید که شما تنها یک بار میتوانید این بخش را تست کنید.\nشماره هدفتون رو وارد کنید.',
                    reply_markup=CMarkup)
                return vipTest_GetTarget
            else:
                update.message.reply_text('شما یک بار این بخش را امتحان کردید.')
                return ConversationHandler.END
    elif str(bmm) == '1':
        update.message.reply_text('شما از ربات بن شده اید.')
        return ConversationHandler.END


def VipTest_GetTarget(update, context):
    if search('^\+989\d{9}$', update.message.text) == None:
        update.message.reply_text('لطفا شماره هدفتون رو بصورت زیر ارسال کنید.\n+989120000000\n')
    else:
        global phone
        phone = update.message.text
        InsertTarget(phone, update.message.chat_id)
        update.message.reply_text("لطفا تعداد پیام هارا وارد کنید.")

        return vipTest_GetCount

def VipTest_GetCount(update, context):
    ch = update.message.chat_id
    try:
        global count
        count = int(update.message.text)
        update.message.reply_text('درحال اسپم کردن با 26 سرور...')
        while Api.count < count:
            Thread(target=Api.snap, args=[phone]).start()
            Thread(target=Api.shad, args=[phone]).start()
            Thread(target=Api.gap, args=[phone]).start()
            Thread(target=Api.tap30, args=[phone]).start()
            Thread(target=Api.emtiaz, args=[phone]).start()
            Thread(target=Api.divar, args=[phone]).start()
            Thread(target=Api.rubika, args=[phone]).start()
            Thread(target=Api.torob, args=[phone]).start()
            system("killall -HUP tor")
            print('threaded')
            sleep(3)
        Api.count = 0
        c.execute(f''' UPDATE Users SET VipTest="1" WHERE ChatID={ch} ''')
        conn.commit()
        update.message.reply_text(f'{count} اس ام اس به شماره {phone} ارسال شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
        return ConversationHandler.END

    except:
        update.message.text('لطفا یک عدد وارد کنید.')

vipTest_conv = ConversationHandler(
    entry_points=[CommandHandler('Viptest', VipTest_Start)],
    states={
        vipTest_GetTarget : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), VipTest_GetTarget)],
        vipTest_GetCount : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), VipTest_GetCount)],
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)

#####################################VipTest################################################################

#####################################Subset#########################################################

def SubSet(update, context):
    update.message.reply_text(f'''شما برای ویژه کردن حساب خود میتوانید از طریق لینک منحصر به فرد خود 50 نفر را به ربات دعوت کنید و حساب خود را ویژه کنید.

https://t.me/MrSMSBomberBot?start={update.message.chat_id}''')

#####################################Subset#########################################################

#####################################info#########################################################

def info(update, context):
    sh_msg = ""
    infos = c.execute(f''' SELECT * FROM Users WHERE ChatID="{update.message.chat_id}" ''')
    for i in infos:
        sh_msg += f"نام: {i[1]}\n"
        if str(i[2]) == '0': sh_msg += "تست بخش ویژه: انجام نشده\n"
        elif str(i[2]) == '1': sh_msg += "تست بخش ویژه: انجام شده\n"
        sh_msg += f"تعداد زیر مجموعه: {i[4]}\n"
        if str(i[5]) == '0': sh_msg += "بخش ویژه: غیر فعال\n"
        elif str(i[5]) == '1': sh_msg += "بخش ویژه: فعال\n"
        sh_msg += f"لینک دعوت دیگران:\nhttps://t.me/MrSMSBomberBot?start={update.message.chat_id}"
    update.message.reply_text(sh_msg)

#####################################info#########################################################

#<//#####################################AdminPanel#############################################################
#</#############SendToAll######################################
global Admin_Chatid
Admin_Chatid = 820586182

sendToAll_get, sendToAll_ok = range(2)

ok_keyboard = [["تایید"], ["لغو"]]
ok_markup = ReplyKeyboardMarkup(ok_keyboard, resize_keyboard=True)

def SendToAll(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لظفا پیام مورد نظر خود را ارسال کنید تا به تمام کاربران ارسال شود.', reply_markup=CMarkup)

        return sendToAll_get
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def SendToAll_Get(update, context):
    global msMood
    global message
    global caption
    if update.message.photo != []:
        msMood = 'photo'
        message = update.message.photo[0].file_id
        caption = update.message.caption
    elif update.message.video != None:
        msMood = 'video'
        message = update.message.video.file_id
        caption = update.message.caption
    elif update.message.document != None:
        msMood = 'document'
        message = update.message.document.file_id
        caption = update.message.caption
    elif update.message.text != None:
        msMood = 'text'
        message = update.message.text
    update.message.reply_text('آیا مطمعن هستید؟', reply_markup=ok_markup)

    return sendToAll_ok

def SendToAll_OK(update, context):
    if update.message.text == "تایید":
        users = c.execute(''' SELECT ChatID FROM Users ''')
        for user in users:
            user = int(user[0])
            try:
                if msMood == 'photo':
                        context.bot.send_photo(user, message, caption=caption)
                elif msMood == 'video':
                    context.bot.send_video(user, message, caption=caption)
                elif msMood == 'document':
                    context.bot.send_document(user, message, caption=caption)
                elif msMood == 'text':
                    context.bot.send_message(user, message)
            except:pass
        update.message.reply_text('پیام به همه کاربران ارسال شد.', reply_markup=ReplyKeyboardRemove(CKeyboard))

        return ConversationHandler.END


sendToAll_conv = ConversationHandler(
    entry_points=[CommandHandler("Sendtoall", SendToAll)],
    states={
        sendToAll_get : [MessageHandler(Filters.all & ~Filters.regex('^لغو$'), SendToAll_Get)],
        sendToAll_ok : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), SendToAll_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\#############SendToAll######################################
#</############ForwardToAll####################################

forwardToAll_Get, forwardToAll_OK = range(2)

def ForwardToAll(update, context):
    if update.message.chat_id == Admin_Chatid:
        update.message.reply_text('پیام خود را ارسال کنید تا برای همه کاربران ارسال شود.', reply_markup=CMarkup)
        return forwardToAll_Get

def ForwardToAll_Get(update, context):
    global mid
    mid = update.message.message_id
    global fid
    fid = update.message.chat_id
    update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

    return forwardToAll_OK

def ForwardToAll_OK(update, context):
    if update.message.text == 'تایید':
        users = c.execute(''' SELECT ChatID FROM Users ''')
        for user in users:
            user = int(user[0])
            context.bot.forward_message(chat_id=user, from_chat_id=fid, message_id=mid)
        update.message.reply_text('پیام به همه کاربران فوروارد شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))

        return ConversationHandler.END

forwardToAll_conv = ConversationHandler(
    entry_points=[CommandHandler("Forwardtoall", ForwardToAll)],
    states={
        forwardToAll_Get : [MessageHandler(Filters.forwarded, ForwardToAll_Get)],
        forwardToAll_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), ForwardToAll_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\############ForwardToAll####################################

#</############SeeUsers########################################

def SeeUsers(update, context):
    if update.message.chat_id == Admin_Chatid:
        show_msg = ""
        all = c.execute(''' SELECT * FROM Users ''')
        for user in all:
            show_msg += f'''آیدی عددی: {user[0]}
یوزرنیم: {user[1]}
تست ویپ: {user[2]}
آخرین هدف: {user[3]}
تعداد زیر مجموعه: {user[4]}
لایسنس: {user[5]}
بن: {user[6]}
------------------------------\n'''
        update.message.reply_text(show_msg)

#<\############SeeUsers########################################

#</############GetDB########################################
def GetDB(update, context):
    if update.message.chat_id == Admin_Chatid:
        context.bot.send_document(update.message.chat_id, open('BombDB.db', 'rb'))
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
#<\############GetDB########################################

#</###########BanSB#########################################\>

banSB_GetID, banSB_OK = range(2)

def BanSB_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید.', reply_markup=CMarkup)

        return banSB_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def BanSB_GetID(update, context):
    try:
        global BanID
        BanID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return banSB_OK
    except:
        update.message.reply_text('نامعتبر است.')

def BanSB_OK(update, context):
    if update.message.text == 'تایید':
        bm = c.execute(f""" SELECT BanMood FROM Users WHERE ChatID="{BanID}" """)
        for i in bm:bm=i[0]
        if str(bm) == '0':
            c.execute(f''' UPDATE Users SET BanMood="1" WHERE ChatID="{BanID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {BanID} با موفقیت بن شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))

            return ConversationHandler.END
        elif str(bm) == '1':
            update.message.reply_text(f'کاربر {BanID} از قبل مسدود بود.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
            return ConversationHandler.END

BanSB_conv = ConversationHandler(
    entry_points=[CommandHandler('BanSB', BanSB_Start)],
    states={
        banSB_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), BanSB_GetID)],
        banSB_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), BanSB_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\############BanSB#######################################/>

#</###########UnBanSB#########################################\>

unbanSB_GetID, unbanSB_OK = range(2)

def UnBanSB_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید.', reply_markup=CMarkup)

        return banSB_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def UnBanSB_GetID(update, context):
    try:
        global UnBanID
        UnBanID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return banSB_OK
    except:
        update.message.reply_text('نامعتبر است.')

def UnBanSB_OK(update, context):
    if update.message.text == 'تایید':
        bm = c.execute(f""" SELECT BanMood FROM Users WHERE ChatID="{UnBanID}" """)
        for i in bm:bm=i[0]
        if str(bm) == '1':
            c.execute(f''' UPDATE Users SET BanMood="0" WHERE ChatID="{UnBanID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {UnBanID} با موفقیت از بن درآمد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))

            return ConversationHandler.END
        elif str(bm) == '0':
            update.message.reply_text(f'کاربر {UnBanID} از قبل آزاد بود.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
            return ConversationHandler.END

UnBanSB_conv = ConversationHandler(
    entry_points=[CommandHandler('UnBanSB', UnBanSB_Start)],
    states={
        banSB_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UnBanSB_GetID)],
        banSB_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UnBanSB_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)

#<\###########UnBanSB#########################################/>

#</###########UpToLicense#########################################\>
upToLicense_GetID, upToLicense_OK = range(2)

def UpToLicense_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید تا حساب کاربری او ویژه شود.', reply_markup=CMarkup)

        return upToLicense_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def UpToLicense_GetID(update, context):
    try:
        global UpToLicenseID
        UpToLicenseID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return banSB_OK
    except:
        update.message.reply_text('نامعتبر است.')

def UpToLicense_OK(update, context):
    if update.message.text == 'تایید':
        bm = c.execute(f""" SELECT License FROM Users WHERE ChatID="{UpToLicenseID}" """)
        for i in bm:bm=i[0]
        if str(bm) == '0':
            c.execute(f''' UPDATE Users SET License="1" WHERE ChatID="{UpToLicenseID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {UpToLicenseID} با موفقیت ویژه شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
            context.bot.send_message(int(UpToLicenseID), text='حساب کاربری شما ویژه شد.')

            return ConversationHandler.END
        elif str(bm) == '1':
            update.message.reply_text(f'کاربر {UpToLicenseID} از قبل ویژه بود.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
            return ConversationHandler.END

UpToLicense_conv = ConversationHandler(
    entry_points=[CommandHandler('UpToLicense', UpToLicense_Start)],
    states={
        banSB_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UpToLicense_GetID)],
        banSB_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UpToLicense_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\###########UpTolicense#########################################/>

#</###########DownTolicense#########################################\>
downToLicense_GetID, downToLicense_OK = range(2)

def DownToLicense_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید تا حساب کاربری او عادی شود.', reply_markup=CMarkup)

        return upToLicense_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def DownToLicense_GetID(update, context):
    try:
        global UpToLicenseID
        UpToLicenseID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return banSB_OK
    except:
        update.message.reply_text('نامعتبر است.')

def DownToLicense_OK(update, context):
    if update.message.text == 'تایید':
        bm = c.execute(f""" SELECT License FROM Users WHERE ChatID="{UpToLicenseID}" """)
        for i in bm:bm=i[0]
        if str(bm) == '1':
            c.execute(f''' UPDATE Users SET License="0" WHERE ChatID="{UpToLicenseID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {UpToLicenseID} با موفقیت عادی شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))

            return ConversationHandler.END
        elif str(bm) == '0':
            update.message.reply_text(f'کاربر {UpToLicenseID} از قبل عادی بود.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
            return ConversationHandler.END

DownToLicense_conv = ConversationHandler(
    entry_points=[CommandHandler('DownToLicense', DownToLicense_Start)],
    states={
        banSB_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), DownToLicense_GetID)],
        banSB_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), DownToLicense_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\###########DownTolicense#########################################/>

#<\\#####################################AdminPanel#############################################################

dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('SeeUsers', SeeUsers))
dp.add_handler(CommandHandler('GetDB', GetDB))
dp.add_handler(CommandHandler('subset', SubSet))
dp.add_handler(CommandHandler('info', info))
dp.add_handler(BanSB_conv)
dp.add_handler(UnBanSB_conv)
dp.add_handler(UpToLicense_conv)
dp.add_handler(DownToLicense_conv)
dp.add_handler(oneApi_conv)
dp.add_handler(vip_conv)
dp.add_handler(vipTest_conv)
dp.add_handler(sendToAll_conv)
dp.add_handler(forwardToAll_conv)
dp.add_handler(CommandHandler('help', help))

updater.start_polling()
updater.idle()