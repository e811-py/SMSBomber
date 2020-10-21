from telegram.ext import CommandHandler, Updater, ConversationHandler, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import pymongo, json, sqlite3
from re import search

conn = sqlite3.connect('BombDB.db', check_same_thread=False)
c = conn.cursor()

connect = pymongo.MongoClient("mongodb://localhost:27017")
DB = connect['SMSBomber']
Users = DB['Users']
#</########Keyboards##################\>
laghv_keyboard = [["لغو"]]
laghv_markup = ReplyKeyboardMarkup(laghv_keyboard, resize_keyboard=True)
admin_Mkeyboard = [['ارسال پیام به همه کاربران', 'ارسال پیام به تک کاربر'],['مشاهده لیست کاربران', 'دانلود دیتابیس'],['بن کردن', 'آزاد کردن'],['ویژه کردن', 'عادی کردن'],['اضافه کردن ضد اسپم','حذف کردن ضد اسپم'],['برگشت']]
admin_Mmarkup = ReplyKeyboardMarkup(admin_Mkeyboard, resize_keyboard=True)
#<\########Keyboards##################/>
#</#############SendToAll######################################
global Admin_Chatid
Admin_Chatid = 820586182

sendToAll_get, sendToAll_ok = range(2)

ok_keyboard = [["تایید"], ["لغو"]]
ok_markup = ReplyKeyboardMarkup(ok_keyboard, resize_keyboard=True)

def SendToAll(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لظفا پیام مورد نظر خود را ارسال کنید تا به تمام کاربران ارسال شود.', reply_markup=laghv_markup)

        return sendToAll_get
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def SendToAll_Get(update, context):
    # print(update.message.forward_date)
    global msMood
    global message
    global caption
    if update.message.forward_date != None:
        msMood = 'forward'
        message = update.message.message_id
        caption = update.message.chat_id
    elif update.message.photo != []:
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
        for user in Users.find():
            user = int(user['_id'])
            try:
                if msMood == 'forward':
                    context.bot.forward_message(chat_id=user, from_chat_id=caption, message_id=message)
                elif msMood == 'photo':
                    context.bot.send_photo(user, message, caption=caption)
                elif msMood == 'video':
                    context.bot.send_video(user, message, caption=caption)
                elif msMood == 'document':
                    context.bot.send_document(user, message, caption=caption)
                elif msMood == 'text':
                    context.bot.send_message(user, message)
            except:pass
        update.message.reply_text('پیام به همه کاربران ارسال شد.', reply_markup=admin_Mmarkup)

        return ConversationHandler.END

def Laghv(update, context):
    if update.message.chat_id == Admin_Chatid:
        update.message.reply_text('برگشتید', reply_markup=admin_Mmarkup)
        return ConversationHandler.END

sendToAll_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^ارسال پیام به همه کاربران$"), SendToAll)],
    states={
        sendToAll_get : [MessageHandler(Filters.all & ~Filters.regex('^لغو$'), SendToAll_Get)],
        sendToAll_ok : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), SendToAll_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\#############SendToAll######################################
#</############ForwardToAll####################################

# forwardToAll_Get, forwardToAll_OK = range(2)
#
# def ForwardToAll(update, context):
#     if update.message.chat_id == Admin_Chatid:
#         update.message.reply_text('پیام خود را ارسال کنید تا برای همه کاربران ارسال شود.', reply_markup=laghv_markup)
#         return forwardToAll_Get
#
# def ForwardToAll_Get(update, context):
#     global mid
#     mid = update.message.message_id
#     global fid
#     fid = update.message.chat_id
#     update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)
#
#     return forwardToAll_OK
#
# def ForwardToAll_OK(update, context):
#     if update.message.text == 'تایید':
#         users = c.execute(''' SELECT ChatID FROM Users ''')
#         for user in users:
#             user = int(user[0])
#             context.bot.forward_message(chat_id=user, from_chat_id=fid, message_id=mid)
#         update.message.reply_text('پیام به همه کاربران فوروارد شد.', reply_markup=ReplyKeyboardRemove(ok_keyboard))
#
#         return ConversationHandler.END
#
# forwardToAll_conv = ConversationHandler(
#     entry_points=[CommandHandler("Forwardtoall", ForwardToAll)],
#     states={
#         forwardToAll_Get : [MessageHandler(Filters.forwarded, ForwardToAll_Get)],
#         forwardToAll_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), ForwardToAll_OK)]
#     },
#     fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
# )
#<\############ForwardToAll####################################

#</############SeeUsers########################################

def SeeUsers(update, context):
    if update.message.chat_id == Admin_Chatid:
        f = open('users.txt', 'w')
        show_msg = ""
        UC = 0
        for user in Users.find():
            UC += 1
            show_msg += f'''id: {user['_id']}
یوزرنیم: {user['Username']}
تست ویپ: {user['TestVip']}
 هدف ها:{user['Requests']}
تعداد زیر مجموعه: {user['Subset']}
لایسنس: {user['VipMode']}
بن: {user['Ban']}
آخرین فعالیت: {user['lastF']}
------------------------------\n'''
        show_msg += f'all Users = {UC}'
        f.write(show_msg)
        f.close()
        context.bot.send_document(update.message.chat_id, open('users.txt', 'rb'), caption=f'تعداد کل کاربران: {UC}')
        del f, show_msg, UC
            # if len(show_msg) > 3500:
            #     update.message.reply_text(show_msg, parse_mode='html')
            #     show_msg = ""
        # update.message.reply_text(show_msg + f"\nتعداد کل کاربران: {count}", parse_mode='html')


#<\############SeeUsers########################################

#</############GetDB########################################
def GetDB(update, context):
    if update.message.chat_id == Admin_Chatid:
        with open('DataBase.json', 'w') as file:
            for user in Users.find():
                userw = json.dumps(user)
                file.write(f'{userw}\n')
            file.close()
        context.bot.send_document(update.message.chat_id, open('DataBase.json', 'rb'))
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
#<\############GetDB########################################

#</###########BanSB#########################################\>

banSB_GetID, banSB_OK = range(2)

def BanSB_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید.', reply_markup=laghv_markup)

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
        for user in Users.find({'_id':int(BanID)}):
            bm = user['Ban']
        if not bm:
            # c.execute(f''' UPDATE Users SET BanMood="1" WHERE ChatID="{BanID}" ''')
            Users.find_one_and_update({'_id':BanID}, {"$set":{'Ban': True}})
            update.message.reply_text(f'کاربر {BanID} با موفقیت بن شد.', reply_markup=admin_Mmarkup)

            return ConversationHandler.END
        elif bm:
            update.message.reply_text(f'کاربر {BanID} از قبل مسدود بود.', reply_markup=admin_Mmarkup)
            return ConversationHandler.END
        else:
            update.message.reply_text('این کاربر در دیتابیس نیست.', reply_markup=admin_Mmarkup)
            return ConversationHandler.END

BanSB_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^بن کردن$"), BanSB_Start)],
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
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید.', reply_markup=laghv_markup)

        return unbanSB_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def UnBanSB_GetID(update, context):
    try:
        global UnBanID
        UnBanID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return unbanSB_OK
    except:
        update.message.reply_text('نامعتبر است.')

def UnBanSB_OK(update, context):
    if update.message.text == 'تایید':
        for i in Users.find({'_id':int(UnBanID)}): bm=i['Ban']
        if bm:
            Users.find_one_and_update({'_id':UnBanID}, {'$set':{'Ban':False}})
            update.message.reply_text(f'کاربر {UnBanID} با موفقیت از بن درآمد.', reply_markup=admin_Mmarkup)

            return ConversationHandler.END
        elif not bm:
            update.message.reply_text(f'کاربر {UnBanID} از قبل آزاد بود.', reply_markup=admin_Mmarkup)
            return ConversationHandler.END
        else:
            update.message.reply_text('این کاربر در دیتابیس نیست.', reply_markup=admin_Mmarkup)
            return ConversationHandler.END

UnBanSB_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^آزاد کردن$"), UnBanSB_Start)],
    states={
        unbanSB_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UnBanSB_GetID)],
        unbanSB_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UnBanSB_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)

#<\###########UnBanSB#########################################/>

#</###########UpToLicense#########################################\>
upToLicense_GetID, upToLicense_OK = range(2)

def UpToLicense_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید تا حساب کاربری او ویژه شود.', reply_markup=laghv_markup)

        return upToLicense_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def UpToLicense_GetID(update, context):
    try:
        global UpToLicenseID
        UpToLicenseID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return upToLicense_OK
    except:
        update.message.reply_text('نامعتبر است.')

def UpToLicense_OK(update, context):
    if update.message.text == 'تایید':
        for i in Users.find({'_id':UpToLicenseID}): bm=i['VipMode']
        if not bm:
            Users.find_one_and_update({'_id':UpToLicenseID}, {"$set":{"VipMode":True}})
            update.message.reply_text(f'کاربر {UpToLicenseID} با موفقیت ویژه شد.', reply_markup=admin_Mmarkup)
            try:
                context.bot.send_message(int(UpToLicenseID), text='حساب کاربری شما ویژه شد.')
            except:
                update.message.reply_text('کاربر ربات را بلاک کرده است.', reply_markup=admin_Mmarkup)

            return ConversationHandler.END
        elif bm:
            update.message.reply_text(f'کاربر {UpToLicenseID} از قبل ویژه بود.', reply_markup=admin_Mmarkup)
            return ConversationHandler.END
        else:
            update.message.reply_text('این کاربر در دیتابیس نیست.', reply_markup=admin_Mmarkup)
            return ConversationHandler.END

UpToLicense_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^ویژه کردن$"), UpToLicense_Start)],
    states={
        upToLicense_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UpToLicense_GetID)],
        upToLicense_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), UpToLicense_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\###########UpTolicense#########################################/>

#</###########DownTolicense#########################################\>
downToLicense_GetID, downToLicense_OK = range(2)

def DownToLicense_Start(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لطفا آیدی عددی کاربر را ارسال کنید تا حساب کاربری او عادی شود.', reply_markup=laghv_markup)

        return downToLicense_GetID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def DownToLicense_GetID(update, context):
    try:
        global DownToLicenseID
        DownToLicenseID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return downToLicense_OK
    except:
        update.message.reply_text('نامعتبر است.')

def DownToLicense_OK(update, context):
    if update.message.text == 'تایید':
        Users.find_one_and_update({'_id':DownToLicenseID}, {'$set': {'VipMode':False}})
        update.message.reply_text(f'کاربر {DownToLicenseID} با موفقیت عادی شد.', reply_markup=admin_Mmarkup)

        return ConversationHandler.END

DownToLicense_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^عادی کردن$"), DownToLicense_Start)],
    states={
        downToLicense_GetID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), DownToLicense_GetID)],
        downToLicense_OK : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), DownToLicense_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\###########DownTolicense#########################################/>

sendToOne_getID, sendToOne_getPM, sendToOne_ok = range(3)

def SendToOne(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        update.message.reply_text('لظفا آیدی عددی کاربر مورد نظر را وارد کنید.', reply_markup=laghv_markup)

        return sendToOne_getID
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def SendToOne_GetID(update, context):
    try:
        global SmsgID
        SmsgID = int(update.message.text)
        update.message.reply_text("لطفا پیام مورد نظر را وارد کنید.")

        return sendToOne_getPM
    except:
        update.message.reply_text('لطفا یک آیدی عددی وارد کنید.')

def SendToOne_GetPM(update, context):
    global msMood
    global message
    global caption
    if update.message.forward_date != None:
        msMood = 'forward'
        message = update.message.message_id
        caption = update.message.chat_id
    elif update.message.photo != []:
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

    return sendToOne_ok

def SendToAll_OK(update, context):
    if update.message.text == "تایید":
        if msMood == 'forward':
            context.bot.forward_message(chat_id=SmsgID, from_chat_id=caption, message_id=message)
            update.message.reply_text('پیام به کاربر مورد نظر ارسال شد.', reply_markup=admin_Mmarkup)
        elif msMood == 'photo':
            context.bot.send_photo(SmsgID, message, caption=caption)
            update.message.reply_text('پیام به کاربر مورد نظر ارسال شد.', reply_markup=admin_Mmarkup)
        elif msMood == 'video':
            context.bot.send_video(SmsgID, message, caption=caption)
            update.message.reply_text('پیام به کاربر مورد نظر ارسال شد.', reply_markup=admin_Mmarkup)
        elif msMood == 'document':
            context.bot.send_document(SmsgID, message, caption=caption)
            update.message.reply_text('پیام به کاربر مورد نظر ارسال شد.', reply_markup=admin_Mmarkup)
        elif msMood == 'text':
            context.bot.send_message(SmsgID, message)
            update.message.reply_text('پیام به کاربر مورد نظر ارسال شد.', reply_markup=admin_Mmarkup)

        return ConversationHandler.END

def Laghv(update, context):
    if update.message.chat_id == Admin_Chatid:
        update.message.reply_text('برگشتید', reply_markup=admin_Mmarkup)
        return ConversationHandler.END

sendToOne_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^ارسال پیام به تک کاربر$"), SendToOne)],
    states={
        sendToOne_getID : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), SendToOne_GetID)],
        sendToOne_getPM:[MessageHandler(Filters.all & ~Filters.regex('^لغو$'), SendToOne_GetPM)],
        sendToOne_ok : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), SendToAll_OK)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
##############################################################################

#</#######################AddNoSpamNumber#################################\>
AddNoSpam_getNumber, AddNoSpam_add = range(2)

def AddNoSpam(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        with open('NoSpamNumbers.txt', 'r') as ree:
            show = ree.read()
            ree.close()
        update.message.reply_text(f'لطفا شماره مورد نظر را وارد کنید.\nلیست فعلی:\n{show}', reply_markup=laghv_markup)
        del show

        return AddNoSpam_add
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def AddNoSpam_Add(update, context):
    if search('^\+989\d{9}$', update.message.text) == None :
        update.message.reply_text('لطفا شماره را بصورت +989120000000 وارد کنید.')
    else:
        with open('NoSpamNumbers.txt', 'a+') as filee:
            filee.write(f',{update.message.text}')
            filee.close()
        update.message.reply_text(f'شماره {update.message.text} در لیست اضافه شد.', reply_markup=admin_Mmarkup)

        return ConversationHandler.END

AddNoSpam_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^اضافه کردن ضد اسپم$"), AddNoSpam)],
    states={
        AddNoSpam_add : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), AddNoSpam_Add)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#<\#######################AddNoSpamNumber#################################/>
RemNoSpam_getNumber, RemNoSpam_rem = range(2)

def RemNoSpam(update, context):
    if int(update.message.chat_id) == Admin_Chatid:
        with open('NoSpamNumbers.txt', 'r') as ree:
            show = ree.read()
            ree.close()
        update.message.reply_text(f'لطفا شماره مورد نظر را وارد کنید.\nلیست فعلی:\n{show}', reply_markup=laghv_markup)
        del show

        return RemNoSpam_rem
    else:
        update.message.reply_text('شما به این بخش دسترسی ندارید.')
        return ConversationHandler.END

def RemNoSpam_Rem(update, context):
    if search('^\+989\d{9}$', update.message.text) == None :
        update.message.reply_text('لطفا شماره را بصورت +989120000000 وارد کنید.')
    else:
        with open('NoSpamNumbers.txt', 'r') as filee:
            lis = filee.read().split(',')
            filee.close()
        lis.remove(update.message.text)
        lis.remove('')
        ftw = ''
        for i in lis:
            ftw += f',{i}'
        with open('NoSpamNumbers.txt', 'w') as filee:
            filee.write(ftw)
            filee.close()
        update.message.reply_text(f'شماره {update.message.text} از لیست حذف شد.', reply_markup=admin_Mmarkup)

        return ConversationHandler.END

RemNoSpam_conv = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("^حذف کردن ضد اسپم$"), RemNoSpam)],
    states={
        RemNoSpam_rem : [MessageHandler(Filters.text & ~Filters.regex('^لغو$'), RemNoSpam_Rem)]
    },
    fallbacks=[MessageHandler(Filters.regex('^لغو$'), Laghv)]
)
#</#######################RemoveNoSpamNumber#################################\>
#<\#######################RemoveNoSpamNumber#################################/>