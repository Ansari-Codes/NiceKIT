from Classes.Tables.Users import USERS

async def signup(data: dict):
    '''Signup Function. Takes `data`:
    
    
    >>> data = {
    >>>     "name": <VARIABLE>,
    >>>     "email: <VARIABLE>,
    >>>     "password: <VARIABLE>
    >>> }
    
    **Returns:** \n\tClasses.Base.Response
    '''
    name = data.get("name", "").value.strip().lower()
    email = data.get("email", "").value.strip().lower()
    pswd = data.get("password", "").value.strip()
    res = await USERS.add_user(name=name, email=email, password=pswd)
    return res
