from Utils.pages import page
from Pages import *

page(SIGNUP)(create_signup)
page(LOGIN)(create_login)
page(SESSION_SET)(set_cookie)
page(SESSION_DEL)(del_cookie)
page(THEME_SET)(set_theme_cookie)
page(MAIN)(create_welcome)
page(DASHBOARD)(create_dashboard)
