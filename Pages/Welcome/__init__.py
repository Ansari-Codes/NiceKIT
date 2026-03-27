from Utils.pages import Request
from Utils.misc import thecode
import app
from Pages.Welcome.WelcomeHeader import create_welcome_header
from Elements.ui import DarkMode

async def create_welcome(request: Request):
    await app.context.client.connected()
    token = request.cookies.get("auth_token")
    DarkMode(thecode(request.cookies.get("dark", None)))
    await create_welcome_header(token)
