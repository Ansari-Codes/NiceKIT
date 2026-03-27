from Utils.pages import Request
from Utils.misc import thecode
from Elements.ui import Drawer, Div, Button, Label, RawCol, AddSpace, navigate, DarkMode
from Pages import SESSION_DEL
from Pages.Dashboard.Home import create_home
from Pages.Dashboard.Section import create_section
from Pages.Dashboard.Settings import create_settings
import app

upper_side_buttons = {
    "Dashboard": {
        "icon": "dashboard",
        "function": create_home
    },
    "A Section": {
        "icon": "image",
        "function": create_section
    },
}
lower_side_buttons = {
    "Settings": {
        "icon": "settings",
        "function": create_settings
    },
    "LogOut": {
        "icon": "exit",
        "function": lambda **kwargs: navigate(SESSION_DEL)
    },
}
functions = {k.lower().strip().replace(' ', '-'):v.get("function") for k,v in {**upper_side_buttons, **lower_side_buttons}.items()}

async def change_page(function, area, kwargs):
    async def F():pass
    f = function or F
    area.clear()
    with area:
        await f(**kwargs)

async def SideDrawer(area, **kwargs):
    d = Drawer().classes("bg-primary")
    with d:
        Label("Dashboard").classes("w-full border-b-2 text-4xl text-center")
        with RawCol().classes("w-full h-full gap-1"):
            for btn, kw in upper_side_buttons.items():
                Button(
                    btn.title(),
                    on_click=lambda kw=kw: change_page(kw.get("function"), area, kwargs), 
                    config={"icon":kw.get("icon")}
                ).classes("w-full")
            AddSpace()
            for btn, kw in lower_side_buttons.items():
                Button(
                    btn.title(),
                    on_click=lambda kw=kw: change_page(kw.get("function"), area, kwargs), 
                    config={"icon":kw.get("icon"), "color": "secondary"}
                ).classes("w-full")
    return d

async def create_dashboard(request: Request, page: str = "dashboard"):
    await app.context.client.connected()
    dark = request.cookies.get("dark", None)
    DarkMode(thecode(request.cookies.get("dark", None)))
    area = Div()
    drawer = await SideDrawer(area, request=request)
    with area:
        if page in functions:
            await functions[page](request) # type:ignore
        else:
            Label("Error 404 - Page not found!")