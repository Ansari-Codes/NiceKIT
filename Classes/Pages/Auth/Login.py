from Classes.Base import Variable, VGroup, Response

class LoginData(VGroup):
    def __init__(self):
        super().__init__("Login")
        self.add_var(Variable("", "identifier"))
        self.add_var(Variable("", "password"))
        self.error_labels = {}

    def verify(self):
        sc = Response()
        if not self.identifier.__str__().strip():
            sc.errors["identifier"] = "Identifier is required!"
        if not self.password.__str__().strip():
            sc.errors["password"] = "Password is required!"
        for field in sc.errors:
            if field in self.error_labels:
                self.error_labels[field].set_text(sc.errors[field])
        return sc

    def get_data(self):
        return {
            "identifier": self.identifier,
            "password": self.password
        }
