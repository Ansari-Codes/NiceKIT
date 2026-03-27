from Elements.ui import Label, DarkMode
from Core.utils import thecode

async def create_section(request):
    DarkMode(thecode(request.cookies.get("dark", None)))
    Label(f"this is simple section")

