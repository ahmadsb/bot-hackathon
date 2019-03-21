import model

import settings
class messages:
    def __init__(self, msg, bot):
        self.msg = msg
        self.bot = bot
        self.storage = model.Storage(settings.HOST, settings.DB)
    def send_to(self, chat_id):
        self.bot.send_message(chat_id=chat_id, text=self.msg)
        pass

    def broadcast(self, room_id):
        # get all chats numbers from db for specific room_id
        users = self.storage.users.find({"room_id":room_id})
        for user in users:
            self.send_to(user['_id'])

