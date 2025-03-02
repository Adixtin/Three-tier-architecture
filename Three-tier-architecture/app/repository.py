from datetime import datetime

class Repository:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def add(self, data) -> dict:
        user = {
            "user_id": self.next_id,
            "firstName": data["firstName"],
            "lastName": data["lastName"],
            "age": datetime.now().year - data["birthYear"],
            "group": data["group"]
        }
        self.users.append(user)
        self.next_id += 1
        return user
                

    def get(self) -> list:
        return self.users
    

    def get_by_id(self, user_id) -> None:
        for user in self.users:
            if user["user_id"] == user_id:
                return user
        return None

    def update(self, user_id, update_data):
        user = self.get_by_id(user_id)
        if user:
            for key, value in update_data.items():
                if key == "birthYear":
                    user["age"] = datetime.now().year - value
                    user[key] = value
                elif key in user:
                    user[key] = value
            return user
        return None

    def delet(self, user_id):
        user = self.get_by_id(user_id)
        if user:
            self.users = [u for u in self.users if u["user_id"] != user_id]
            return user
        return None
        
        
        
