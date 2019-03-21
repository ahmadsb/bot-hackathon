from telegram import ParseMode

from messages import messages

class messageBold(messages):

    def __init__(self,msg, bot):
        super().__init__(msg,bot)

    def send_to(self, chat_id):
        self.bot.send_message(chat_id=chat_id, text=self.msg, parse_mode=ParseMode.MARKDOWN)
        pass