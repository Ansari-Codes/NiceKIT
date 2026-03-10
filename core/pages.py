from app import nui,context
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, HTMLResponse

page = nui.page
def per_page():
    context.client.layout.classes("w-screen h-screen !m-0 !p-0", remove="nicegui-layout")
    context.client.page_container.classes("w-screen h-screen !m-0 !p-0")
    context.client.content.classes("w-screen h-screen !m-0 !p-0", remove="nicegui-content")
    nui.add_head_html('<link rel="stylesheet" type="text/css" href="/static/styles.css">')
    return context.client.content
