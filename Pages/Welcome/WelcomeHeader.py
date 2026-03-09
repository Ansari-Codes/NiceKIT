from ui import Header, RawRow, AddSpace,navBar, Label, Button, Link
from app import NAME, FAVICON
from Pages import DASHBOARD, LOGIN, SIGNUP
from Backend.Auth.Session import get_current_user

async def addButtons(res, desktop, mobile):
    auth = res.success and res.response
    if not auth:
        with desktop:
            Button("LogIn", link=LOGIN)
            Button("SignUp", link=SIGNUP)
        with mobile:
            Button("LogIn", link=LOGIN)
            Button("SignUp", link=SIGNUP)
    else:
        with desktop: Button("Dashboard", link=DASHBOARD)
        with mobile: Button("Dashboard", link=DASHBOARD)
    desktop.update()
    mobile.update()

async def create_welcome_header(token):
    with Header():
        with RawRow().classes("w-full"):
            Label(FAVICON + NAME).classes("w-fit text-xl font-bold")
            AddSpace()
            with RawRow().classes("w-fit gap-2"):
                _, desktop, mobile = navBar()
    res = await get_current_user(token)
    await addButtons(res, desktop, mobile)
