from Elements.ui import Label, DarkMode
from Utils.misc import thecode

async def create_home(request):
    user_id = request.cookies.get("user_id")
    user_name = request.cookies.get("user_name")
    DarkMode(thecode(request.cookies.get("dark", None)))
    Label(f"Hi! {user_name.title()}").classes("w-full font-bold text-9xl text-primary")

