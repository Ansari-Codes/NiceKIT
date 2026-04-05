from Elements.ui import Label, Notify, Button, Input, TabArea, Tab, TabPanel, TabPanels, RawRow, navigate, Choice, DarkMode
from Pages import SESSION_SET, DASHBOARD, THEME_SET
from Classes.Pages.Dashboard.Settings import SettingsData
from Backend.Dashboard.Settings import update_settings
from Utils.misc import thecode

async def input_section(label, model, inps):
    with RawRow().classes("w-full gap-2"):
        Label(label).classes("text-md font-semibold")
        inp = Input(model).classes("w-full")
    inps.append(inp)
    return inp

async def create_settings(area, request):
    # theme
    dark = thecode(request.cookies.get("dark", None))
    theme_controller = DarkMode(dark)
    # cookies
    user_id = request.cookies.get("user_id", None)
    # setup
    setdata = SettingsData(user_id)
    setdata_inps = []
    print(dark)
    async def save():
        for i in setdata_inps: i.disable()
        try:
            res = setdata.verify()
            if not res.success:
                for e,ee in res.errors.items():
                    Notify(f"{e.upper()}: {ee}", type="negative")
            else:
                user_settings = await update_settings(setdata.get_data())
                if user_settings.success:
                    for i in setdata_inps: i.set_value("")
                    Notify("Changes saved successfully!", type="positive")
                    if user_settings.response:
                        navigate(
                            SESSION_SET, id=user_id, 
                            name=user_settings.response.user_name, #type:ignore
                            redirect_to=DASHBOARD+'?page=dashboard')
                else:
                    for e,ee in user_settings.errors.items():
                        Notify(f"{e.upper()}: {ee}", type="negative")
        except Exception as e:
            Notify(f"Error: {e}", type="negative")
        finally:
            for i in setdata_inps: i.enable()
    # The ui goes here
    with TabArea("account") as settings_tab_area:
        account = Tab("account", "Account", "person")
        theme = Tab("theme", "Theme", icon="format_paint")
    with TabPanels(settings_tab_area, value=account).classes("w-full h-full"):
        with TabPanel(account):
            await input_section("New Username (Optional)", setdata.user_name, setdata_inps)
            await input_section("New Email (Optional)", setdata.email, setdata_inps)
            await input_section("New Password (Optional)", setdata.password, setdata_inps)
            await input_section("Password (Required)", setdata.previous_password, setdata_inps)
            Button("Save", on_click=save).classes("w-full")
        with TabPanel(theme):
            theme_map = {
                "Dark": True,
                "Light": False,
                "System": None
            }
            reverse_theme_map = {v: k for k, v in theme_map.items()}
            def change_theme(x):
                value = theme_map[x.value]
                navigate(
                    THEME_SET, dark=value, #type:ignore
                    redirect_to=DASHBOARD+'?page=settings')
            theme_controller.set_value(dark)
            Choice(
                ["Dark", "Light", "System"],
                value=reverse_theme_map[dark],
                on_change=change_theme
            )
