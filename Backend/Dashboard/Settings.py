from Classes.Tables.Users import USERS, User
from Classes.Base import Response

async def update_settings(data: dict):
    '''Function to update settings of user. Takes `data`:
    
    
    >>> data = {
    >>>     "user_id": <INTEGER>,
    >>>     "new_user_name": <VARIABLE>,
    >>>     "new_email": <VARIABLE>,
    >>>     "new_password": <VARIABLE>,
    >>>     "new_avatar": <VARIABLE>,
    >>>     "previous_password": <VARIABLE>,
    >>> }
    
    **Returns:** \n\tClasses.Base.Response
    '''
    user_id = data.get("user_id", "")
    new_user_name = data.get("new_user_name", "")
    new_email = data.get("new_email", "")
    new_avatar = data.get("new_avatar", "")
    new_password = data.get("new_password", "")
    previous_password = data.get("previous_password", "")
    user = await USERS.get(user_id.value)
    res = Response()
    update_dict = {}
    if new_user_name.value.strip():
        update_dict['name'] = new_user_name.value.strip().lower()
    if new_email.value.strip():
        update_dict['email'] = new_email.value.strip().lower()
    if new_avatar.value.strip():
        update_dict['avatar'] = new_avatar.value.strip().lower()
    if new_password.value.strip():
        update_dict['password'] = new_password.value.strip().lower()
    if user:
        if user.user_password == previous_password.value:
            await user.update(**update_dict)
            res.response = user.from_row({
                    "name": new_user_name.value, 
                    "email": new_email.value, 
                    "password": new_password.value, 
                    "avatar": new_avatar.value
                })
        else:
            res.errors['password'] = "Password is not correct!"
    else:
        res.errors['Error'] = f"User not found with id `{user_id}`!"
    return res