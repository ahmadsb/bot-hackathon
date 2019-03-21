# YOUR BOT LOGIC/STORAGE/BACKEND FUNCTIONS HERE
from pymongo.mongo_client import MongoClient


class Storage:
    def __init__(self, host, db):
        self.client = MongoClient(host)
        self.db = self.client.get_database(db)
        self.users = self.db.get_collection("users")
        self.logs = self.db.get_collection("logs")
        self.rooms = self.db.get_collection("rooms")

        # self.users.create_index("chat_id")

    def add_user(self, chat_id, language, first_name, last_name, room_id="General_Room"):
        # if not last_name:
        #     last_name = " "
        # if not first_name:
        #     first_name = " "
        tmp = {"_id": chat_id, "$set": {'language': language, 'first_name': first_name, 'last_name': last_name}}
        if not tmp in self.users.find({"_id": chat_id}):
            self.users.update_one({"_id": chat_id},
                                  {"$set": {'language': language, 'first_name': first_name, 'last_name': last_name,
                                            'room_id': room_id}},
                                  upsert=True)

    def get_users(self):
        memebrs = []
        for i in self.users.find():
            memebrs.append(i['first_name'] + " " + i['last_name'])
        return memebrs

    # def add_user(self language, first_name, last_name):
    #     tmp = { "$set": {'language': language, 'first_name': first_name, 'last_name': last_name}}
    #     if not tmp in self.users.find({"_id": chat_id}):
    #         self.users.update_one({"_id": chat_id},
    #                               {"$set": {'language': language, 'first_name': first_name, 'last_name': last_name}},
    #                               upsert=True)
