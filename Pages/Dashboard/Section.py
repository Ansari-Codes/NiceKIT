from Elements.ui import Label, DarkMode
from Utils.misc import thecode

async def create_section(request):
    DarkMode(thecode(request.cookies.get("dark", None)))
    Label(f"this is simple section")
    Label(str(request.cookies))
