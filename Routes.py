from Core.pages import page
from Pages import *

page(SIGNUP)(create_signup)
page(SESSION_SET)(set_cookie)
page(SESSION_DEL)(del_cookie)
page(MAIN)(create_welcome)
