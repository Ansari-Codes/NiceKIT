from datetime import datetime
from string import ascii_letters, digits, punctuation
from uuid import uuid4
from random import random
from app import ui
import re

def time_ago(ts):
    now = datetime.now()
    dt = datetime.fromisoformat(ts)
    diff = now - dt
    seconds = diff.total_seconds()
    if seconds < 60: return "Just now"
    elif seconds < 3600: return f"{int(seconds//60)} min ago"
    elif seconds < 86400: return f"{int(seconds//3600)} hr ago"
    else: return dt.strftime("%d %b %Y")

def Loading(text=None, spinner={"type":"box", "size": "lg", "color":"primary"}, rs="r"):
    text = text or "Loading..."
    with ui.row().classes("w-full h-full justify-center items-center") as r:
        ui.spinner(**spinner)
        h = ui.html(text, sanitize=lambda x:x)
    if rs == 'r': return r
    elif rs == 'rh': return r,h
    return r,h

def randomstr(max=6): return uuid4().hex[:max]
def rnd(l=6): return ''.join([f'{random().__str__().split(".")[0]}' for i in range(l)])

def verifyUsername(name: str):
    if not name:
        return False
    for i in name:
        if i not in digits + ascii_letters + ' _-.':
            return False
    return True

def verifyMail(mail: str):
    return re.match(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        mail
    ) is not None

def verifyPswd(password: str) -> bool:
    strength = 0
    strength += any(c.isalpha() for c in password)
    strength += any(c in punctuation for c in password)
    strength += any(c.isdigit() for c in password)
    strength += (len(password) >= 8)
    return strength == 4

def escsql(s) -> str:
    return str(s).replace("'", "''")
