import json
import random
from uuid import uuid4
from time import time
from os import mkdir
AVATAR_IMG = """iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAABmJLR0QA/wD/AP+gvaeTAAAACXBI
WXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4gwfDg4yBhjr5QAAABl0RVh0Q29tbWVudABDcmVhdGVk
IHdpdGggR0lNUFeBDhcAAACbSURBVHja7dEBDQAACMMwwL/nI4OEdBLWTpLSWWMBAAACAEAAAAgA
AAEAIAAABACAAAAQAAACAEAAAAgAAAEAIAAABACAAAAQAAACAEAAAAgAAAEAIAAABACAAAAQAAAC
AEAAAAgAAAEAIAAABACAAAAAIAAABACAAAAQAAACAEAAAAgAAAEAIAAABACAAAAQAAACAEAAAAjA
hxYN1AS8uZ5NRAAAAABJRU5ErkJggg==
"""

class HipchatGenerator:
    def __init__(self, args):
        self.args = args
        pass
    
    def start(self):
        if not self.args.email:
            raise Exception("No email provided for users")
        metadata = self.create_metadata()
        users = self.create_users()
        rooms = self.create_rooms(users)
        room_history = self.create_room_history(rooms, users)
        for dir in ["./dump", "./dump/rooms", "./dump/users", "./dump/users/files"]:
            try:
                mkdir(dir)
            except FileExistsError:
                pass
            except Exception as ex:
                raise ex
        # Write to files
        with open("./dump/users.json", "w", encoding="utf-8") as fuser:
            fuser.write(json.dumps(users, indent=2))

        with open("./dump/rooms.json", "w", encoding="utf-8") as froom:
            froom.write(json.dumps(rooms, indent=2))

        with open("./dump/metadata.json", "w", encoding="utf-8") as fmeta:
            fmeta.write(json.dumps(metadata, indent=2))

        for id, history in room_history.items():
            r_path = "./dump/rooms/{}".format(id)
            mkdir(r_path)
            mkdir(r_path + "/files")
            with open(r_path + "/history.json", "w", encoding="utf-8") as fhistory:
                fhistory.write(json.dumps(history, indent=2))



    def create_users(self):
        users = []
        for uid in range(1, self.args.users+1):
            users.append(
                {
                    "User": {
                        "account_type": "user",
                        "avatar": AVATAR_IMG,
                        "created": "",
                        "email": self.args.email,
                        "id": uid,
                        "is_deleted": False,
                        "mention_name": "dummy_{}".format(uid),
                        "name": "Mr. Dummy #{}".format(uid),
                        "roles": [
                            "users"
                        ],
                        "timezone": "UTC",
                        "title": "" # XXX: Not used?
                    }
                }
            )
        return users

    def create_rooms(self, users):
        rooms = []
        for rid in range(1, self.args.rooms+1):
            is_private = random.choice([True, False])
            owner = random.choice(users)
            owner = owner["User"]["id"]
            members = set()
            if is_private:
                members.add(owner)
                for nuser in range(random.randint(1, len(users) / 2)):
                    members.add(users[random.randint(0, len(users) -1)]["User"]["id"])
            rooms.append(
                  {
                    "Room": {
                        "created": "2015-05-22T15:59:56+00:00",
                        "guest_access_url": None,
                        "id": rid,
                        "is_archived": False,
                        "members": list(members),
                        "name": "Room numero #{}".format(rid),
                        "owner": owner,
                        "participants": [],
                        "privacy": "private" if is_private else "public",
                        "topic": "Toooooooooopic!"
                    }
                },
            )
        return rooms

    def create_metadata(self):
        return {
            "Metadata": {
                "coral_api": "v2",
                "end_date": None,
                "includes_attachments": True,
                "includes_emoticons": True,
                "includes_legal": True,
                "includes_messages": True,
                "includes_oto": True,
                "start_date": None,
                "timestamp": time(),
                "version": "1"
            }
        }
    
    def create_room_history(self, rooms, users):
        history = {}
        for room in rooms:
            members = None
            if len(room["Room"]["members"]) == 0:
                members = []
                for u in users:
                    members.append(u["User"]["id"])
            else:
                members = room["Room"]["members"]
            history[room["Room"]["id"]] = []
            for mi in range(0, random.randint(self.args.min_msgs, self.args.max_msgs)):
                history[room["Room"]["id"]].append(
                    {
                        "UserMessage": {
                            "attachment": None,
                            "attachment_path": None,
                            "id": uuid4(),
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
        return history