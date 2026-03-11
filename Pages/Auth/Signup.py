from Elements.ui import Card, Input, Button, Label, navigate, RawCol, RawRow, Password, Notify, AddSpace, navigate
from Core.pages import per_page, Request
from Classes.Auth import SignupData
from Backend.Auth.Signup import signup
from Pages import SESSION_SET

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

async def sup(widgets, sdata, error_labels, redirect_to):
    for w in widgets: w.disable()
    try:
        response = sdata.verify()
        if response.success:
            res = await signup(sdata.get_data())
            user = res.response
            if res.success: 
                Notify(f"Success!", type="positive")
            else:
                for k, error in res.errors.items():
                    if k in error_labels: error_labels[k].set_text(error)
                    else:Notify(f"{k.upper()}: {error.capitalize()}", type="negative")
                return
            navigate(SESSION_SET, id=user.user_id, name=user.user_name, redirect_to=redirect_to)#type:ignore
        else:
            for k, error in response.errors.items():
                if k in error_labels: error_labels[k].set_text(error)
                else:Notify(f"{k.upper()}: {error.capitalize()}", type="negative")
            return
    finally:
        for w in widgets: w.enable()

async def Signup(redirect_to='/'):
    widgets = []
    error_labels = {}
    per_page().classes("flex justify-center items-center")
    sdata = SignupData()
    sdata.error_labels = error_labels
    async def sinup():
        await sup(widgets, sdata, error_labels, redirect_to)
    with Card().classes("max-w-[98vw] sm:max-w-[50vw] md:max-w-[50vw] w-full h-fit"):
        Label("Create Account").classes("w-full text-xl font-bold")
        lblinp("Name", sdata.name, widgets, error_labels)
        lblinp("Email", sdata.email, widgets, error_labels)
        lblinp("Password", sdata.password, widgets, error_labels)
        lblinp("Confirm", sdata.confirm, widgets, error_labels)
        widgets.append(Button("Create", sinup).classes("w-full"))

async def create_signup(request: Request, redirect_to='/'):
    token = request.cookies.get("auth_token")
    if not token: await Signup(redirect_to)
    else: navigate(redirect_to)
