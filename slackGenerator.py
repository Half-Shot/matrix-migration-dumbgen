import json
import string
import random
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

class SlackGenerator:
    def __init__(self, args):
        self.args = args
        pass

    def start(self):
        if not self.args.email:
            raise Exception("No email provided for users")
        users = self.create_users(self.args.user_prefix)
        rooms = self.create_rooms(users, self.args.room_prefix)
        room_history, room_files = self.create_room_history(rooms, users)
        try:
            mkdir("./dump")
        except FileExistsError:
            rmtree("./dump")
            mkdir("./dump")
            pass
        except Exception as ex:
            raise ex

        for dir in rooms:

        # Write to files
        with open("./dump/users.json", "w", encoding="utf-8") as fuser:
            fuser.write(json.dumps(users, indent=2))

        with open("./dump/channels.json", "w", encoding="utf-8") as froom:
            froom.write(json.dumps(rooms, indent=2))

        for id, history in room_history.items():
            print("Saving history for room #", id)
            r_path = "./dump/rooms/{}".format(id)
            mkdir(r_path)
            mkdir(r_path + "/files")
            for room_file in room_files[id]:
                mkdir(r_path + "/files/" + room_file["root"])
                with open(r_path + "/files/" + room_file["path"], "wb") as ffile:
                    ffile.write(''.join(random.choices(string.ascii_letters + string.digits, k=room_file["size"])).encode())
            with open(r_path + "/history.json", "w", encoding="utf-8") as fhistory:
                fhistory.write(json.dumps(history, indent=2))



    def create_users(self, prefix):
        users = []
        have_admin = False
        for uid in range(1, self.args.users+1):
            account_type = "user" if have_admin else "admin"
            have_admin = True
            users.append(
                {
                    "id": uid,
                    "name": "dummy",
                    "is_admin": have_admin,
                    "deleted": false,
                    "created": "",
                    "email": self.args.email,
                    "is_deleted": False,
                    "mention_name": "{}{}".format(prefix, uid),
                    "name": "Mr. Dummy #{}".format(uid),
                    "roles": [
                        "user"
                    ],
                    "timezone": "UTC",
                    "title": "" # XXX: Not used?
                }
            )
        return users

    def create_rooms(self, users, prefix):
        rooms = []
        for rid in range(1, self.args.rooms+1):
            is_private = random.choice([True, False])
            owner = random.choice(users)
            owner = owner["User"]["id"]
            members = set()
            if is_private:
                members.add(owner)
                for nuser in range(random.randint(1, len(users) // 2)):
                    members.add(users[random.randint(0, len(users) -1)]["User"]["id"])
            rooms.append(
                {
                    "created": 1537798089,
                    "id": rid,
                    "is_archived": False,
                    "is_general": False,
                    "members": list(members),
                    "name": "{} #{}".format(prefix, rid),
                    "creator": owner,
                    "topic": {
                        "creator": owner,
                        "value": "Toooooooooopic!",
                        "last_set": 1537798089,
                    }
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
        files = {}
        for room in rooms:
            print("Creating history for room #", room["Room"]["id"])
            members = None
            if len(room["Room"]["members"]) == 0:
                members = []
                for u in users:
                    members.append(u["User"]["id"])
            else:
                members = room["Room"]["members"]
            history[room["Room"]["id"]] = []
            files[room["Room"]["id"]] = []
            for mi in range(0, random.randint(self.args.min_msgs, self.args.max_msgs)):
                attachment = None
                if random.randint(0, 20) == 20:
                    root = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                    path = root + "/attachment.bin"
                    data_size = random.choice([5000, 25000, 100000])
                    attachment = {
                        "name": "attachment.bin",
                        "path": path,
                        "size": data_size,
                        "url": "",
                    }
                    files[room["Room"]["id"]].append({
                        "path": path,
                        "root": root,
                        "size": data_size,
                    })
                history[room["Room"]["id"]].append(
                    {
                        "UserMessage": {
                            "attachment": attachment,
                            "attachment_path": attachment["path"] if attachment is not None else None,
                            "id": str(uuid4()),
                            "mentions": [],
                            "message": "This is a example message generated to test hipchat migrations!",
                            "sender": {
                                "id": random.choice(members),
                                "links": {
                                    "self": "https://api.hipchat.com/v2/user/2189579".format(random.choice(members))
                                },
                                "mention_name": "dummy_?",
                                "name": "Dummy #?",
                                "version": "00000000"
                            },
                            "timestamp": "2015-05-22T16:29:35Z 107493",
                            "type": "user",
                        }
                    }
                )
        return history, files
