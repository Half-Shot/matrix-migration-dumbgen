import json
import string
import random
import requests 
from faker import Faker
from zipfile import ZipFile
from uuid import uuid4
from time import time
from os import mkdir
from shutil import rmtree
AVATAR_IMG = """iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAABmJLR0QA/wD/AP+gvaeTAAAACXBI
WXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4gwfDg4yBhjr5QAAABl0RVh0Q29tbWVudABDcmVhdGVk
IHdpdGggR0lNUFeBDhcAAACbSURBVHja7dEBDQAACMMwwL/nI4OEdBLWTpLSWWMBAAACAEAAAAgA
AAEAIAAABACAAAAQAAACAEAAAAgAAAEAIAAABACAAAAQAAACAEAAAAgAAAEAIAAABACAAAAQAAAC
AEAAAAgAAAEAIAAABACAAAAAIAAABACAAAAQAAACAEAAAAgAAAEAIAAABACAAAAQAAACAEAAAAjA
hxYN1AS8uZ5NRAAAAABJRU5ErkJggg==
"""

room_names = [
    "general",
    "business",
    "slack",
    "matrix",
    "breakout",
    "movingon",
    "marketing",
    "design",
    "engineering"
]

class SlackGenerator:
    def __init__(self, args):
        self.args = args
        if not self.args.email:
            raise Exception("No email provided for users")
        pass

    def start(self):
        with ZipFile(self.args.outfile, 'w') as zip:
            users = self.create_users(self.args.user_prefix)
            zip.writestr("users.json", json.dumps(users, indent=2))
            rooms = self.create_rooms(users, self.args.room_prefix)
            zip.writestr("channels.json", json.dumps(rooms, indent=2))
            room_history = self.create_room_history(rooms, users)
            for id, history in room_history.items():
                zip.writestr(f'{id}/1-1-1.json', json.dumps(history, indent=2))


    def create_users(self, prefix):
        users = []
        fk = Faker()
        for uid in range(1, self.args.users+1):
            req = requests.get('https://dog.ceo/api/breeds/image/random')
            avatar = req.json()['message']
            name = fk.name()
            username = name.split(' ')[0]
            users.append(
                {
                    "id": "U" + str(uid),
                    "name": username.lower(),
                    "real_name": username,
                    "is_admin": uid == 1,
                    "is_owner": uid == 1,
		            "is_bot": False,
                    "deleted": False,
                    "updated": 1603871635,
                    "profile": {
			            "display_name": name,
                        "email": self.args.email,
                        "image_original": avatar,
                    },
                    "title": "" # XXX: Not used?
                }
            )
        return users

    def create_rooms(self, users, prefix):
        rooms = []
        for rid in range(1, self.args.rooms+1):
            owner = random.choice(users)
            owner = owner["id"]
            members = set()
            members.add(owner)
            name = random.choice(room_names) + str(rid)
            for _nuser in range(random.randint(1, len(users) // 2)):
                members.add(users[random.randint(0, len(users) -1)]["id"])
            rooms.append(
                {
                    "created": 1537798089,
                    "id": "C" + str(rid),
                    "is_archived": False,
                    "is_general": False,
                    "members": list(members),
                    "name": name,
                    "creator": owner,
                    "topic": {
                        "creator": owner,
                        "value": "Toooooooooopic!",
                        "last_set": 1537798089,
                    },
                    "purpose": {
                        "creator": owner,
                        "value": "A purpose!",
                        "last_set": 1537798089,
                    }
                },
            )
        return rooms

    def create_room_history(self, rooms, users):
        history = {}
        fk = Faker()
        for room in rooms:
            print("Creating history for room #", room["id"])
            members = room["members"]
            history[room["id"]] = []
            msgtime = 1600000000
            for mi in range(0, random.randint(self.args.min_msgs, self.args.max_msgs)):
                sender = random.choice(members)
                msgtime = msgtime + random.random() * 300000
                history[room["id"]].append({
                    "type": "message",
                    "text": fk.text(),
                    "user": sender,
                    "ts": msgtime,
                })
                # attachment = None
                # if random.randint(0, 20) == 20:
                #     root = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                #     path = root + "/attachment.bin"
                #     data_size = random.choice([5000, 25000, 100000])
                #     attachment = {
                #         "name": "attachment.bin",
                #         "path": path,
                #         "size": data_size,
                #         "url": "",
                #     }
                # history[room["id"]].append(
                #     {
                #         "attachment": attachment,
                #         "attachment_path": attachment["path"] if attachment is not None else None,
                #         "id": str(uuid4()),
                #         "mentions": [],
                #         "message": fk.text(),
                #         "sender": {
                #             "id": random.choice(members),
                #             "mention_name": "dummy_?",
                #             "name": "Dummy #?",
                #             "version": "00000000"
                #         },
                #         "timestamp": "2015-05-22T16:29:35Z 107493",
                #         "type": "user",
                #     }
                # )
        return history
