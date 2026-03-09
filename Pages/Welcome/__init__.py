from Core.pages import Request
import app
from Pages.Welcome.WelcomeHeader import create_welcome_header

async def create_welcome(request: Request):
    await app.context.client.connected()
    token = request.cookies.get("auth_token")
    await create_welcome_header(token)
