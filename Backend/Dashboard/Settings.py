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
    new_user_name = data.get("new_user_name", "").value.strip().lower()
    new_email = data.get("new_email", "").value.strip().lower()
    new_avatar = data.get("new_avatar", "").value
    new_password = data.get("new_password", "").value.strip()
    previous_password = data.get("previous_password", "").value.strip()
    user = await USERS.get(user_id.value)
    res = Response()
    update_dict = {}
    if new_user_name.strip():
        update_dict['name'] = new_user_name
    if new_email.strip():
        update_dict['email'] = new_email
    if new_avatar.strip():
        update_dict['avatar'] = new_avatar
    if new_password.strip():
        update_dict['password'] = new_password
    if user:
        if user.user_password == previous_password:
            await user.update(**update_dict)
            res.response = user.from_row({
                    "name": new_user_name, 
                    "email": new_email, 
                    "password": new_password,
                    "avatar": new_avatar
                })
        else:
            res.errors['password'] = "Password is not correct!"
    else:
        res.errors['Error'] = f"User not found with id `{user_id}`!"
    return res