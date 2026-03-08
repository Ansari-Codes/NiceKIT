from Classes.Base import Variable, VGroup, Success
from Core.utils import verifyMail, verifyPswd, verifyUsername

class LoginData(VGroup):
    '''
    .password
    .identifier
    .error_labels = {
        "identifier": Lable(),
        "password": Lable()
    }
    '''
    def __init__(self):
        super().__init__("Login")
        self.add_var(Variable("", "identifier"))
        self.add_var(Variable("", "password"))
        self.error_labels = {}

    def verify(self):
        sc = Success()
        sc['identifier'] = None
        sc['password'] = None
        if not self.identifier.__str__().strip():
            sc["identifier"] = "Identifier is required!"
            if "identifier" in self.error_labels:
                self.error_labels["identifier"].set_text(sc['identifier'])
        if not self.password.__str__().strip():
            sc["password"] = "Password is required!"
            if "password" in self.error_labels:
                self.error_labels["password"].set_text(sc['password'])
        return sc

    def get_data(self):
        return {
            "identifier": self.identifier,
            "password": self.password
        }

class SignupData(VGroup):
    '''
    .name
    .email
    .password
    .confirm
    .error_labels = {
        "name": Lable(),
        "email": Lable(),
        "password": Lable(),
        "confirm": Lable(),
    }
    '''

    def __init__(self):
        super().__init__("Signup")
        self.add_var(Variable("", "name"))
        self.add_var(Variable("", "email"))
        self.add_var(Variable("", "password"))
        self.add_var(Variable("", "confirm"))
        self.error_labels = {}

    def verify(self):
        sc = Success()
        sc["name"] = None
        sc["email"] = None
        sc["password"] = None
        sc["confirm"] = None
        name = str(self.name).strip()
        email = str(self.email).strip()
        password = str(self.password).strip()
        confirm = str(self.confirm).strip()
        if not name:
            sc["name"] = "Name is required!"
        elif not verifyUsername(name):
            sc["name"] = "Invalid username!"
        if not email:
            sc["email"] = "Email is required!"
        elif not verifyMail(email):
            sc["email"] = "Invalid email address!"
        if not password:
            sc["password"] = "Password is required!"
        elif not verifyPswd(password):
            sc["password"] = "Password is too weak!"
        if not confirm:
            sc["confirm"] = "Confirm password is required!"
        elif confirm != password:
            sc["confirm"] = "Passwords do not match!"
        for field in sc:
            if sc[field] and (field in self.error_labels):
                self.error_labels[field].set_text(sc[field])
        return sc

    def get_data(self):
        return {
            "name": str(self.name),
            "email": str(self.email),
            "password": str(self.password),
        }