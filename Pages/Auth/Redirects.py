from Core.pages import  RedirectResponse, HTMLResponse, Request
from Core.utils import randomstr
from Backend.Auth.Session import save_cookie, delete_cookie

AGE = 15 * 60 * 60 * 24
def addCookie(res, key, value):
    res.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        max_age=AGE
    )

async def set_theme_cookie(dark: str, redirect_to: str = '/'):
    res = RedirectResponse(redirect_to)
    addCookie(res, "dark", dark)
    return res

async def set_cookie(id: int, name: str, redirect_to: str = '/dashboard'):
    res = RedirectResponse(redirect_to)
    id = int(id)
    value = randomstr().__str__()
    try:
        await save_cookie(value, id, AGE)
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    addCookie(res, "auth_token", value)
    addCookie(res, "user_id", str(id))
    addCookie(res, "user_name", str(name))
    addCookie(res, "dark", None)
    return res

async def del_cookie(request:Request):
    res = RedirectResponse('/')
    value = request.cookies.get("auth_token")
    if value is None: return res
    try:
        await delete_cookie(value)
    except Exception as e:
        return HTMLResponse(f"<span style='color: red;font-size:100px;'>An error occured!</span><br><span style='color: gray;font-size:15px;'>{e}</span>")
    res.delete_cookie("auth_token")
    res.delete_cookie("user_id")
    res.delete_cookie("user_name")
    return res
