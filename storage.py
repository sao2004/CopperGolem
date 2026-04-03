import json
import os

class Admins:
    FILE = "admins.json"

    @staticmethod
    def load():
        if not os.path.exists(Admins.FILE):
            return {}
        with open(Admins.FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)

    @staticmethod
    def save(users):
        with open(Admins.FILE, "w") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def add(id, username):
        admins = Admins.load()
        admins[str(id)] = {"username": username}
        Admins.save(admins)
        return True, "Admin added successfully"

    @staticmethod
    def get(id):
        admins = Admins.load()
        return admins.get(str(id))

    @staticmethod
    def get_from_username(username):
        admins = Admins.load()
        for uid, admin in admins.items():
            if admin["username"] == username:
                return {"id": uid, "username": admin["username"]}
        return None

    @staticmethod
    def delete(id):
        admins = Admins.load()
        uid = str(id)
        if uid in admins:
            del admins[uid]
            Admins.save(admins)
            return True, "Admin removed successfully"
        return False, "Admin not found"

    @staticmethod
    def update(id : int, username):
        admins = Admins.load()
        uid = str(id)
        if uid in admins:
            admins[uid]["username"] = username
            Admins.save(admins)
            return True, "Admin updated successfully"
        return False, "Admin not found"

    @staticmethod
    def list() -> list[dict]:
        admins = Admins.load()
        return list(admins.values())

    @staticmethod
    def delete_data():
        with open(Admins.FILE, "w") as f:
            f.write("")

class Users:
    FILE = "users.json"

    @staticmethod
    def load():
        if not os.path.exists(Users.FILE):
            return {}
        with open(Users.FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return {}
            return json.loads(content)

    @staticmethod
    def save(users):
        with open(Users.FILE, "w") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def add(id, username, skill_level, minecraft_username):
        users = Users.load()
        try:
            skill_level = int(skill_level)
        except ValueError:
            return False,"Skill level must be an integer"
        if skill_level < 0 or skill_level > 5:
            return False,"Skill level must be between 0 and 5"
        users[str(id)] = {"username": username, "skill_level": skill_level, "minecraft_username": minecraft_username}
        Users.save(users)
        return True, "User added successfully"

    @staticmethod
    def get(id: int):
        users = Users.load()
        return users.get(str(id))

    @staticmethod
    def get_from_username(username: str):
        users = Users.load()
        for uid, user in users.items():
            if user["username"] == username:
                return {"id": uid, "username": user["username"], "skill_level": user["skill_level"]}
        return None

    @staticmethod
    def get_from_minecraft_username(minecraft_username: str):
        users = Users.load()
        for uid, user in users.items():
            if user["minecraft_username"] == minecraft_username:
                return {"id": uid, "username": user["username"], "skill_level": user["skill_level"], "minecraft_username": user["minecraft_username"]}
        return None


    @staticmethod
    def delete(id : int):
        users = Users.load()
        uid = str(id)
        if uid in users:
            del users[uid]
            Users.save(users)
            return True, "User deleted successfully"
        return False, "User not found"

    @staticmethod
    def update(id : int, username: str | None, skill_level: int | str | None, minecraft_username: str | None):
        users = Users.load()
        uid = str(id)
        if uid not in users:
            return False, "User not found"
        if username is not None:
            users[uid]["username"] = username
        if skill_level is not None:
            try:
                skill_level = int(skill_level)
            except ValueError:
                return False, "Skill level must be an integer"
            if skill_level < 0 or skill_level > 5:
                return False, "Skill level must be between 0 and 5"
            users[uid]["skill_level"] = skill_level
        if minecraft_username is not None:
            users[uid]["minecraft_username"] = minecraft_username
        Users.save(users)
        return True, "User updated successfully"

    @staticmethod
    def list() -> list[dict]:
        users = Users.load()
        return list(users.values())

    @staticmethod
    def delete_data():
        with open(Users.FILE, "w") as f:
            f.write("")

class Challenges:
    FILE = "challenges.json"

    @staticmethod
    def load() -> list[dict]:
        if not os.path.exists(Challenges.FILE):
            return []
        with open(Challenges.FILE, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, dict):
                return list(data.values())
            return data

    @staticmethod
    def save(challenges):
        ordered_challenges = []
        for i, challenge in enumerate(challenges):
            ordered_challenges.append({
                "id": i + 1,
                "difficulty": challenge["difficulty"],
                "text": challenge["text"]
            })
        with open(Challenges.FILE, "w") as f:
            json.dump(ordered_challenges, f, indent=4)

    @staticmethod
    def add(difficulty : int, text : str):
        if difficulty < 1 or difficulty > 5:
            return False, "Difficulty must be between 1 and 5"
        if not text:
            return False, "Please provide a challenge text"
        challenges = Challenges.load()
        challenge = {"difficulty": difficulty, "text": text}
        challenges.append(challenge)
        Challenges.save(challenges)
        return True, "Challenge added successfully"

    @staticmethod
    def get(id : int):
        challenges = Challenges.load()
        for challenge in challenges:
            if challenge["id"] == id:
                return challenge
        return None, "Challenge not found"

    @staticmethod
    def delete(id : int):
        challenges = Challenges.load()
        for i, challenge in enumerate(challenges):
            if challenge["id"] == id:
                del challenges[i-1]
                Challenges.save(challenges)
                return True, "Challenge removed successfully"
        return False, "Challenge not found"

    @staticmethod
    def update(id : int, difficulty : int | None, text : str | None):
        challenges = Challenges.load()
        if difficulty is not None and (difficulty < 1 or difficulty > 5):
            return False, "Difficulty must be between 1 and 5"

        for i, challenge in enumerate(challenges):
            if challenge["id"] == id:
                challenges[i]["difficulty"] = difficulty
                challenges[i]["text"] = text
                Challenges.save(challenges)
                return True, "Challenge updated successfully"
        return False, "Challenge not found"

    @staticmethod
    def delete_data():
        with open(Challenges.FILE, "w") as f:
            f.write("")
