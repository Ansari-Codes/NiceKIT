from Classes.Users import USERS

async def signup(data: dict):
    name = data.get("name")
    email = data.get("email")
    pswd = data.get("password")
    user = await USERS.add_user(name=name, email=email, password=pswd)
    return user
