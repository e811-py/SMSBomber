from telegram.ext import CommandHandler, Updater, ConversationHandler, Filters, MessageHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3

conn = sqlite3.connect('BombDB.db', check_same_thread=False)
c = conn.cursor()
#</########Keyboards##################\>
laghv_keyboard = [["لغو"]]
laghv_markup = ReplyKeyboardMarkup(laghv_keyboard, resize_keyboard=True)
admin_Mkeyboard = [['ارسال پیام به همه کاربران', 'ارسال پیام به تک کاربر'],['مشاهده لیست کاربران', 'دانلود دیتابیس'],['بن کردن', 'آزاد کردن'],['ویژه کردن', 'عادی کردن'],['برگشت']]
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
    print(update.message.forward_date)
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
        users = c.execute(''' SELECT ChatID FROM Users ''')
        for user in users:
            user = int(user[0])
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
        all = c.execute(''' SELECT * FROM Users ''')
        count = 0
        for user in all:
            count += 1
            show_msg += f'''id: {user[0]}
یوزرنیم: {user[1]}
تست ویپ: {user[2]}
آخرین هدف: {user[3]}
تعداد زیر مجموعه: {user[4]}
لایسنس: {user[5]}
بن: {user[6]}
آخرین فعالیت: {user[7]}
------------------------------\n'''
        f.write(show_msg)
        f.close()
        context.bot.send_document(update.message.chat_id, open('users.txt', 'rb'))
        del f, show_msg
            # if len(show_msg) > 3500:
            #     update.message.reply_text(show_msg, parse_mode='html')
            #     show_msg = ""
        # update.message.reply_text(show_msg + f"\nتعداد کل کاربران: {count}", parse_mode='html')


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
        bm = c.execute(f""" SELECT BanMood FROM Users WHERE ChatID="{BanID}" """)
        for y in bm:
            bm = y[0]
        if str(bm) == '0':
            c.execute(f''' UPDATE Users SET BanMood="1" WHERE ChatID="{BanID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {BanID} با موفقیت بن شد.', reply_markup=admin_Mmarkup)

            return ConversationHandler.END
        elif str(bm) == '1':
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
        bm = c.execute(f""" SELECT BanMood FROM Users WHERE ChatID="{UnBanID}" """)
        for i in bm:bm=i[0]
        if str(bm) == '1':
            c.execute(f''' UPDATE Users SET BanMood="0" WHERE ChatID="{UnBanID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {UnBanID} با موفقیت از بن درآمد.', reply_markup=admin_Mmarkup)

            return ConversationHandler.END
        elif str(bm) == '0':
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
        # c.execute(f''' UPDATE Users SET License="1" WHERE ChatID="{UpToLicenseID}" ''')
        # conn.commit()
        # update.message.reply_text(f'کاربر {UpToLicenseID} با موفقیت ویژه شد.', reply_markup=admin_Mmarkup)
        # context.bot.send_message(int(UpToLicenseID), text='حساب کاربری شما ویژه شد.')
        #
        # return ConversationHandler.END
        bm = c.execute(f""" SELECT License FROM Users WHERE ChatID="{UpToLicenseID}" """)
        for i in bm:bm=i[0]
        if str(bm) == '0':
            c.execute(f''' UPDATE Users SET License="1" WHERE ChatID="{UpToLicenseID}" ''')
            conn.commit()
            update.message.reply_text(f'کاربر {UpToLicenseID} با موفقیت ویژه شد.', reply_markup=admin_Mmarkup)
            try:
                context.bot.send_message(int(UpToLicenseID), text='حساب کاربری شما ویژه شد.')
            except:
                update.message.reply_text('کاربر ربات را بلاک کرده است.', reply_markup=admin_Mmarkup)

            return ConversationHandler.END
        elif str(bm) == '1':
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
        global UpToLicenseID
        UpToLicenseID = int(update.message.text)
        update.message.reply_text("آیا مطمعن هستید؟", reply_markup=ok_markup)

        return downToLicense_OK
    except:
        update.message.reply_text('نامعتبر است.')

def DownToLicense_OK(update, context):
    if update.message.text == 'تایید':
        c.execute(f''' UPDATE Users SET License="0" WHERE ChatID="{UpToLicenseID}" ''')
        conn.commit()
        update.message.reply_text(f'کاربر {UpToLicenseID} با موفقیت عادی شد.', reply_markup=admin_Mmarkup)

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
