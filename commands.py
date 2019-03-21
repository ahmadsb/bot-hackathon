import telegram
from py_translator import Translator, LANGUAGES
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import goslate
from messages import messages
import model
import settings
import logging
from googletrans import Translator  # Import Translator module from googletrans package
from MessageBold import messageBold


class Command:

    def __init__(self):
        self.storage = model.Storage(settings.HOST, settings.DB)
        logging.basicConfig(
            format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

    def command_start(self, bot, update):
        chat_id = update.message.chat_id
        first_name = update.message['from_user']['first_name']
        last_name = update.message['from_user']['last_name']

        language = 'en'
        self.logger.info(f"> Start chat #{chat_id}")

        if not self.storage.users.find_one({"_id": chat_id}):
            self.storage.add_user(chat_id, language, first_name, last_name)
        str = Command.getHelp()
        kb = [[telegram.KeyboardButton("/change_lang")]]
        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text=f"Hello {first_name}, and welcome to the multi language bot!\n" + str ,
                         reply_markup=kb_markup)

    # def command_create(self,bot, update,args):
    #     ## put to data base
    #     pass

    # def command_user_details(self,bot, update, args):
    #     user_id = update.message.chat_id
    #     lang = args[0]
    #     #update for user the room id
    def command_lang(self, bot, update, args):
        chat_id = update.message.chat_id
        language = args[0]
        self.storage.users.update_one({"_id": chat_id},
                                      {"$set": {'language': language}},
                                      upsert=True)

    def command_memebers(self, bot, update):
        members = self.storage.users.find()  # return list of string
        user_id = update.message.chat_id
        curr_room_id = self.storage.users.find_one({"_id": user_id})['room_id']

        keyboard = []
        for j, i in enumerate(members):
            if (i['room_id'] == curr_room_id):
                keyboard.append([InlineKeyboardButton(i['first_name'] + " " + i['last_name'], callback_data=f"{j}")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f'Members of *{curr_room_id}*', reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)

    def command_join(self, bot, update, args):
        room_id = args[0]
        chat_id = update.message.chat_id
        prev_room_id = self.storage.users.find_one({"_id": chat_id})['room_id']

        if self.storage.rooms.find_one({"_id": room_id}):
            self.storage.users.update_one({"_id": chat_id},
                                          {"$set": {'room_id': room_id}},
                                          upsert=True)
            msg = messages(f"You have just joined {room_id}, ENJOY!", bot)
            msg.send_to(update.message.chat_id)

            first_name = update.message['from_user']['first_name']
            last_name = update.message['from_user']['last_name']

            msgBroadcast = messages(f"{first_name} {last_name} just joined {room_id}!", bot)
            msgBroadcast.broadcast(room_id)

            msgBroadcast = messages(f"{first_name} {last_name} just left this room!", bot)
            msgBroadcast.broadcast(prev_room_id)
        else:
            msg = messages(f"Room {room_id} does not exist!", bot)
            msg.send_to(update.message.chat_id)

    def command_create(self, bot, update, args):
        room_id = args[0]
        if not self.storage.rooms.find_one({"_id": room_id}):
            self.storage.rooms.update_one({"_id": room_id},
                                          {"$set": {"created_by": update.message.chat_id}},
                                          upsert=True)
            msg = messages(f"Room {room_id} has been successfully created", bot)
            msg.send_to(update.message.chat_id)
        else:
            msg = messages(f"Room {room_id} already exists ", bot)
            msg.send_to(update.message.chat_id)

    @classmethod
    def getHelp(cls):
        commands = {
            '/start': "starts the bot and be in General_Room",
            '/create [room key]': "creates a room ",
            '/join [room key]': "join a room",
            '/members': "show all members in the group",
            '/Change_lang': "change the language , given a list of languages",
            '/lang [language symbole]': "change the language by writing the lang symbol",
            '/help': "get all commands",
        }
        str = ''
        for key, value in commands.items():
            str += key + " : " + value + "\n"
        return str

    def command_help(self, bot, update):
        str = Command.getHelp()
        messages(str, bot).send_to(update.message.chat_id)

    def command_change_lang(self, bot, update):
        kb = []
        langs = sorted(LANGUAGES.keys())
        OFFSET = 127462 - ord('A')
        def flag(code):
            code = code.upper()
            return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

        for key,value in LANGUAGES.items():
            f = settings.lang_dic[key] if key in settings.lang_dic else 'en'
            kb.append([telegram.KeyboardButton("/lang " + key + " " + value.upper() + " " + flag(f))])

        kb_markup = telegram.ReplyKeyboardMarkup(kb, resize_keyboard=True, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id,
                         text="Choose a language please",
                         reply_markup=kb_markup)

        # room_id = int(args[0])
        # user_id = update.message.chat_id
        # first_name = update.message['chat']['first_name']
        # last_name = update.message['chat']['last_name']
        # ### send  username details to database(chat id) for the room and defult lang eng
        # msg = messages(f"{first_name} {last_name} joined ", bot)
        # msg.send_to(user_id)
        # msg.broadcast(room_id)

    def command_respond(self, bot, update):
        user_id = update.message.chat_id
        text = update.message.text
        ##get the room that user uses
        self.logger.info(f"= Got on chat #{user_id}: {text!r}")
        curr_room_id = self.storage.users.find_one({"_id": user_id})['room_id']
        for i in self.storage.users.find():
            userId = int(i['_id'])
            if not (userId == user_id):
                if (i['room_id'] == curr_room_id):
                    ## translate to user lang

                    response = Translator().translate(text, dest=i['language']).text
                    # response = goslate.Goslate().translate(text, i['language'])
                    # response = Translator().translate('text', src='en', dest=i['language'])
                    ## send to users
                    msg = messageBold("*"+update.message['from_user']['first_name']+"*" + " \n"  + response, bot)
                    msg.send_to(userId)

                    # bot.send_message(chat_id=update.message.chat_id, parse_mode=ParseMode.,
                    #                  text=f"*{user_name}* {flag('us')}\nI'm a bot, please talk to me!")
