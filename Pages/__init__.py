SIGNUP = '/signup'
LOGIN = '/login'
MAIN = '/'
DASHBOARD = '/dashboard'
SESSION_SET = '/set-cookie'
SESSION_DEL = '/del-cookie'

from Pages.Auth import create_signup
from Pages.Auth import set_cookie, del_cookie
from Pages.Welcome import create_welcome
