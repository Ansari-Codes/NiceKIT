from Classes.Tables.Users import USERS

async def login(data: dict):
    '''Login Function. Takes `data`:
    
    
    >>> data = {
    >>>     "identifier": <VARIABLE>,
    >>>     "password: <VARIABLE>
    >>> }
    
    **Returns:** \n\tClasses.Base.Response
    '''
    identifier = data.get("identifier", "")
    pswd = data.get("password", "")
    user = await USERS.login(identifier=identifier.value, password=pswd.value)
    return user
