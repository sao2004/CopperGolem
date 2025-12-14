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
        for admin in admins.values():
            if admin["username"] == username:
                return admin
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
    def add(id, username, skill_level):
        users = Users.load()
        try:
            skill_level = int(skill_level)
        except ValueError:
            return False,"Skill level must be an integer"
        if skill_level < 0 or skill_level > 5:
            return False,"Skill level must be between 0 and 5"
        users[str(id)] = {"username": username, "skill_level": skill_level}
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
    def delete(id : int):
        users = Users.load()
        uid = str(id)
        if uid in users:
            del users[uid]
            Users.save(users)
            return True, "User deleted successfully"
        return False, "User not found"

    @staticmethod
    def update(id : int, username: str | None, skill_level: int | str | None):
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

if __name__ == "__main__":
    if __name__ == "__main__":
        print("=== USERS TESTS ===")

        # Add users
        print("\nAdding user 1 with invalid skill 10")
        success, msg = Users.add(1, "Alice", 10)
        print(success, msg)

        print("\nAdding user 1 with valid skill 3")
        success, msg = Users.add(1, "Alice", 3)
        print(success, msg)

        print("\nAdding user 2 with valid skill 4")
        success, msg = Users.add(2, "Bob", 4)
        print(success, msg)

        # Get users
        print("\nGetting user 1")
        print(Users.get(1))

        # Update users
        print("\nUpdating user 1 with invalid skill 20")
        success, msg = Users.update(1, skill_level=20, username=None)
        print(success, msg)

        print("\nUpdating user 1 with valid skill 5 and new username 'AliceUpdated'")
        success, msg = Users.update(1, skill_level=5, username="AliceUpdated")
        print(success, msg)

        print("\nGetting updated user 1")
        print(Users.get(1))

        # Delete user
        print("\nDeleting user 1")
        success, msg = Users.delete(1)
        print(success, msg)

        print("\nTrying to get deleted user 1")
        print(Users.get(1))


        print("\n=== CHALLENGES TESTS ===")

        # Add challenges
        print("\nAdding challenge 1")
        success, msg = Challenges.add(1, "Jump over lava")
        print(success, msg)

        print("\nAdding challenge 2")
        success, msg = Challenges.add(3, "Build a castle")
        print(success, msg)

        # List all challenges
        print("\nListing all challenges")
        print(Challenges.load())

        # Update challenge
        print("\nUpdating challenge 1 difficulty to 2 and text to 'Cross the lava pit'")
        success, msg = Challenges.update(1, difficulty=2, text="Cross the lava pit")
        print(success, msg)

        print("\nGetting updated challenge 1")
        print(Challenges.get(1))

        # Delete challenge
        print("\nDeleting challenge 2")
        success, msg = Challenges.delete(2)
        print(success, msg)

        print("\nListing all challenges after deletion")
        print(Challenges.load())
