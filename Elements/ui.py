from app import nui
from typing import Callable, Literal
from urllib.parse import urlencode

def navigate(link: str, new_tab: bool = False, **params):
    if params:
        query = urlencode(params)
        link = f"{link}?{query}"
    nui.navigate.to(link, new_tab)
def Label(text="", model=None, model_configs=None):
    lbl = nui.label(text)
    if model:
        model_configs = model_configs or {}
        lbl.bind_text(model, target_name='value', **model_configs)
    return lbl
def DarkMode(dark=None, on_change=lambda x=None:x):
    return nui.dark_mode(dark, on_change=on_change)

def Div(): return nui.element('Div')
def Header(): return nui.header(fixed=True, elevated=False)
def Html(html: str): return nui.html(html, sanitize=lambda x:x)
def Col(): return nui.column()
def Row(): return nui.row()
def RawCol(): return nui.element().classes("flex flex-col")
def RawRow(): return nui.element().classes("flex flex-row")
def Center(): return nui.element( ).classes("flex justify-center items-center" )
def Footer(config: dict|None = None): return nui.footer(**(config or {}))
def Card(align: Literal['start', 'end', 'center', 'baseline', 'stretch']|None = None ):
    return nui.card(align_items=align).classes("bg-card-l dark:bg-card-d gap-1 p-3")
def CardSec(): return nui.card_section()
def CardAct(): return nui.card_actions()
def Drawer(side: Literal['left', 'right'] = 'left', **kwargs): 
    return nui.drawer(side, **kwargs)
def TabArea(value= None, on_change: Callable|None=None): 
    return nui.tabs(value=value, on_change=on_change)
def Tab(name, label='', icon=''): return nui.tab(name, label, icon)
def TabPanels(tabs=None, *, value=None, on_change=None, animated=True, keep_alive=True): 
    return nui.tab_panels(tabs, value=value, on_change=on_change, keep_alive=keep_alive, animated=animated)
def TabPanel(name): return nui.tab_panel(name)
def Expansion(): return nui.expansion()

def Link(
        text: str = "",
        link: str = "",
        underline:  bool = True,
        new_tab: bool = False,
    ):
    return nui.link(text, link, new_tab).classes("hover:underline"*underline)

def Choice(choices:list|dict, value, **kwargs):
    return nui.toggle(choices, value=value, **kwargs)

def Input(
        model = None,
        default_props: bool|None = True,
        bindings: dict|None = None,
        type: Literal['text', 'color', 'number', 'file'] = 'text',
        **kwargs
    ):
    bindings = bindings or {}
    inp = None
    if type == "text": inp = nui.input(**kwargs)
    elif type == "color": inp = nui.color_input(**kwargs)
    elif type == 'number': inp = nui.number(**kwargs)
    else: inp = nui.input().props(f'type="{type}"')
    if inp:
        inp.classes("bg-inp rounded-sm")
        inp.props('input-class="text-text-secondary"')
        inp.props("dense outlined"*bool(default_props) + ' ')
        if model: inp.bind_value(model, 'value', **bindings)
    return inp

def Password(password_toggle_button=True, **kwargs):
    return Input(**kwargs, password=True, password_toggle_button=password_toggle_button)

def Select(
        model = None,
        options: list|dict|None = None,
        default_props: bool|None = True,
        bindings: dict|None = None,
        **kwargs
    ):
    bindings = bindings or {}
    slc = nui.select(options=options or [], **kwargs)
    slc.props("dense outlined"*bool(default_props) + ' ')
    if model: slc.bind_value(model, 'value', **bindings)
    slc.classes("bg-inp rounded-sm").props('input-class="text-text-secondary"')
    return slc

def Button(
        text: str = "", 
        on_click = lambda: (),
        link="",
        new_tab=False,
        config: dict|None = None
    ):
    if not config: config = {}
    btn = nui.button(text=text, on_click=on_click, **config)
    if link:
        btn.props(f'href="{link}"')
    if new_tab:
        btn.props(f'target="_blank"')
    return btn.props("glossy")

def TextArea(
        content: str = "",
        model=None,
        autogrow: bool = False,
        max_h: str|None = None,
        min_h: str|None = None,
        overflow: str|None = None,
        flexible: bool = False,
        config: dict|None = None,
        inp_cls: str = "",
        inp_prp: str = "",
        inp_sty: str = "",
    ):
    if not config: config = {}
    ta = nui.input(value=content, **config)
    inner_classes = ""
    if model: ta.bind_value(model)
    if flexible: inner_classes += " flex-grow flex-shrink resize-none"
    if min_h: inner_classes += f" min-h-[{min_h}]"
    if max_h: inner_classes += f" max-h-[{max_h}]"
    if overflow: inner_classes += f" overflow-{overflow}"
    if autogrow: ta.props('autogrow')
    ta.classes(inner_classes)
    ta.props('dense outlined')
    ta.classes("bg-inp rounded-sm").props(f'input-class="{inp_cls}" input-props="{inp_prp}" input-style="{inp_sty}"')
    return ta

def CheckBox(
        text:str = "",
        value:bool = False,
        on_change:Callable = lambda x:()
    ):
    return nui.checkbox(text, value=value, on_change=on_change)

def AddSpace():
    return nui.space()

def Icon(
        name: str = "" , 
        size: str|None = None,
        color: str|None = None,
    ):
    return nui.icon(name, size=size, color=color)

def Notify(
        message:str = '', 
        position:Literal['top-left', 'top-right', 'bottom-left', 
                         'bottom-right', 'top', 'bottom', 'left', 
                         'right', 'center'
                        ]='bottom',
        close_button='✖', 
        **kwargs
    ): nui.notify(message, position=position, close_button=close_button, **kwargs)

def Dialog():
    return nui.dialog().props('backdrop-filter="hue-rotate(10deg)"')

class logger(nui.html):    
    def __init__(self, content: str = '', *, sanitize: Callable[[str], str] | Literal[False] = lambda x:x, tag: str = 'div') -> None:
        super().__init__(content, sanitize=sanitize, tag=tag)
    def print(self, line: str, classes="", props="", style=""):
        self.content = f'{self.content}<p class="{classes}" {props} style="{style}">{line}</p>'
        self.update()

def Logger():
    return logger()

def confirm(statement="", on_yes=None, on_no=None):
    d = Dialog().props("persistent")
    with d:
        with Card():
            Label(statement).classes("text-md font-semibold")
            with Row():
                Button("Yes", config=dict(icon='check'), on_click=on_yes)
                Button("No", config=dict(icon='close'), on_click=on_no or d.delete)
    return d

def navBar(links: dict | None = None, bkp="sm"):
    links = links or {}
    norm_links = {}
    for name, opts in links.items():
        if not isinstance(opts, dict):
            norm_links[name] = {"link": opts, "cond": True}
        else:
            norm_links[name] = opts.copy()

    with nui.element().classes("w-fit h-fit") as nav:
        with nui.element().classes(f"items-center justify-between gap-2 hidden {bkp}:!flex", remove='hidden') as desktop:
            for name, opts in norm_links.items():
                if opts.get("cond", True):  # use get instead of pop
                    Button(name, **{k: v for k, v in opts.items() if k != "cond"})

        with Button(config=dict(icon="menu")).classes(f"flex {bkp}:hidden"):
            with nui.menu().props("auto-close"):
                with RawCol().classes("w-[150px] gap-1 p-2 bg-secondary") as mobile:
                    for name, opts in norm_links.items():
                        if opts.get("cond", True):  # again, just read
                            Button(name, **{k: v for k, v in opts.items() if k != "cond"}).classes("w-full")

    return nav, desktop, mobile
