SIGNUP = '/signup'
LOGIN = '/login'
MAIN = '/'
DASHBOARD = '/dashboard'
SESSION_SET = '/set-cookie'
SESSION_DEL = '/del-cookie'
THEME_SET = '/set-theme-cookie'

from Pages.Auth import create_signup
from Pages.Auth import create_login
from Pages.Auth import set_cookie, del_cookie, set_theme_cookie
from Pages.Welcome import create_welcome
from Pages.Dashboard import create_dashboard
