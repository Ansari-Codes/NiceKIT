from Classes.Users import USERS

async def login(data: dict):
    identifier = data.get("identifier", "")
    pswd = data.get("password", "")
    user = await USERS.login(identifier=identifier, password=pswd)
    return user
