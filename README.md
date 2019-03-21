# AMORE Bot 🤖
Multilingual Translation Bot <https://t.me/MultiLangGroupBot>
* Ahmad Sabbah
* Rashid Khamis
* Odai Odeh
* Majd AbuHattoum
<br><br>
<a href="https://t.me/MultiLangGroupBot"><img src="https://www.botcide.com/wp-content/uploads/2018/07/bot_icon_240_001-1.png" align="left" hspace="5" vspace="3" width="90"></a>

**AMORE Bot** is a friendly Telegram chatbot that enables users to have a multilingual translation of chats on the fly, connecting people from all over the world!
<br><br>

## Features
- Simultaneous translation of more than 100 languages
- Create and join chat rooms.
- Show other members in the room
- Adds a layer of anonymity
- Friendly interface 

## Screenshots
### Start command
<img src="screenshots/command_start.jpg" alt="drawing" width="350"/>

### Change language command
<img src="screenshots/command_change_land.jpg" alt="drawing" width="350"/>

### Join room command
<img src="screenshots/command_join.jpg" alt="drawing" width="350"/>

## How to Run This Bot
### Prerequisites
* Python 3.7
* pipenv
* MongoDB

### Setup
* Clone this repo from github
* Install dependencies: `pipenv install`
* Get a BOT ID from the [botfather](https://telegram.me/BotFather).
* Create a `secret_settings.py` file:
        BOT_TOKEN = "your-bot-token-here"
### Run
To run the bot use:
    pipenv run python bot.py
(Or just `python bot.py` if running in a pipenv shell.)

## Credits and References
* [Telegram Docs](https://core.telegram.org/bots)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* [py-translator](https://pypi.org/project/py-translator)
