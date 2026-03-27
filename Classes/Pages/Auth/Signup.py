from Classes.Base import Variable, VGroup, Response
from Utils.misc import verifyMail, verifyPswd, verifyUsername

class SignupData(VGroup):
    def __init__(self):
        super().__init__("Signup")
        self.add_var(Variable("", "name"))
        self.add_var(Variable("", "email"))
        self.add_var(Variable("", "password"))
        self.add_var(Variable("", "confirm"))
        self.error_labels = {}

    def verify(self):
        sc = Response()
        sc.errors["name"] = None
        sc.errors["email"] = None
        sc.errors["password"] = None
        sc.errors["confirm"] = None
        name = str(self.name.value).strip().lower()
        email = str(self.email.value).strip().lower()
        password = str(self.password.value).strip()
        confirm = str(self.confirm.value).strip()
        if not name:
            sc.errors["name"] = "Name is required!"
        elif not verifyUsername(name):
            sc.errors["name"] = "Invalid username!"
        if not email:
            sc.errors["email"] = "Email is required!"
        elif not verifyMail(email):
            sc.errors["email"] = "Invalid email address!"
        if not password:
            sc.errors["password"] = "Password is required!"
        elif not verifyPswd(password):
            sc.errors["password"] = "Password is too weak!"
        if not confirm:
            sc.errors["confirm"] = "Confirm password is required!"
        elif confirm != password:
            sc.errors["confirm"] = "Passwords do not match!"
        for field in sc.errors:
            if field in self.error_labels:
                self.error_labels[field].set_text(sc.errors[field])
        return sc

    def get_data(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
