from ui import Card, Row, Col, Input, Button, Label, CardAct, CardSec, navigate, RawCol, RawRow, Div, Password, Notify, AddSpace
from Core.pages import per_page, Request
from Classes.Auth import SignupData
from Backend.Auth.Signup import signup

def lblinp(label, model, widgets, error_labels, password=False):
    with RawCol().classes("w-full h-fit p-0.5"):
        with RawRow().classes("h-fit w-full"):
            label_wdiget = Label(label).classes("capitalize max-w-fit w-fit")
            AddSpace()
            error_wdiget = Label().classes("text-sm items-center text-red-500")
            error_labels[label.lower()] = error_wdiget
        if password: input_widget = Password(model=model)
        else: input_widget = Input(model)
        widgets.append(input_widget)
    return label_wdiget, error_wdiget, input_widget

async def Signup(redirect_to='/'):
    widgets = []
    error_labels = {}
    async def sup():
        for w in widgets: w.disable()
        try:
            response = sdata.verify()
            if response.success:
                res = await signup(sdata.get_data())
                if res.success: 
                    Notify(f"Successful signup!", type="positive")
                    return
                else:
                    for k, error in res.errors.items():
                        if k in error_labels: error_labels[k].set_text(error)
                        else: Notify(f"{k.upper()}: {error.capitalize()}", type="negative")
        finally:
            for w in widgets: w.enable()
    per_page().classes("flex justify-center items-center")
    sdata = SignupData()
    sdata.error_labels = error_labels
    with Card().classes("max-w-[98vw] sm:max-w-[70vw] md:max-w-[60vw] h-fit"):
        with CardSec().classes("flex w-full h-fit items-center justify-center"):
            Label("Create Account").classes("text-xl font-bold")
        with CardSec().classes("flex w-full h-fit items-center justify-center"):
            lblinp("Name", sdata.name, widgets, error_labels)
            lblinp("Email", sdata.email, widgets, error_labels)
            lblinp("Password", sdata.password, widgets, error_labels)
            lblinp("Confirm", sdata.confirm, widgets, error_labels)
        with CardAct().classes("flex w-full h-fit items-center justify-center"):
            widgets.append(Button("Create", sup).classes("w-full"))

async def create_signup(redirect_to='/'):
    token = None
    if not token: await Signup(redirect_to)
    else: navigate(redirect_to)
