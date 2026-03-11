from Classes.Tables.Sessions import SESSIONS
from Classes.Tables.Users import USERS
from Classes.Base import Response
import time

async def save_cookie(value, userId, max_age):
    '''Saves cookie to database. Takes:
    
    1. value: The token string
    2. userId: The id of the user whose session is to be created.
    3. max_age: Maximum age of this session.
    
    **Returns:** Classes.Base.Response.success (bool)
    '''
    expires_at = int(time.time() + max_age)
    res = await SESSIONS.add_token(
        user=userId,
        token=value,
        expires_at=expires_at
    )
    return res.success

async def delete_cookie(value):
    '''Delete cookie from the database. Takes `value`, the token string.
    
    **Returns:** bool
    '''

    try:
        response = await SESSIONS.get_session(value)
        if not response.success:
            return False
        await response.response.delete() # type:ignore
        return True
    except Exception:
        return False

async def get_current_user(token):
    '''Get user from session token. Takes `token`, the token string.
        
    **Returns:** Classes.Base.Response
    '''
    res = Response()
    res = await SESSIONS.get_session(token)
    if res.success:
        user = await USERS.get(res.response.session_user) # type:ignore
        res.response = user
    return res
