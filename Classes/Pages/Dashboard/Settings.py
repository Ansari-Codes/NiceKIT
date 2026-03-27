from Classes.Base import Variable, VGroup, Response
from Core.utils import verifyUsername, verifyPswd, verifyMail

class SettingsData(VGroup):
    def __init__(self, user_id):
        super().__init__("Settings")
        self.add_var(Variable(user_id, "user_id"))
        self.add_var(Variable("", "user_name"))
        self.add_var(Variable("", "email"))
        self.add_var(Variable("", "avatar"))
        self.add_var(Variable("", "password"))
        self.add_var(Variable("", "previous_password"))
        self.error_labels = {}

    def verify(self):
        sc = Response()
        if not self.previous_password.value.strip():
            sc.errors['prev_pass'] = "Password is required!"
        if (self.user_name.value) and (not verifyUsername(self.user_name.value)):
            sc.errors['user_name'] = "User name is not valid!"
        if (self.email.value) and (not verifyMail(self.email.value)):
            sc.errors['email'] = "Email is not valid!"
        if (self.password.value) and (not verifyPswd(self.password.value)):
            sc.errors['pass'] = "Password is weak!"
        for field in sc.errors:
            if field in self.error_labels:
                self.error_labels[field].set_text(sc.errors[field])
        return sc

    def get_data(self):
        return {
            "user_id": self.user_id,
            "new_user_name": self.user_name,
            "new_email": self.email,
            "new_avatar": self.avatar,
            "previous_password": self.previous_password,
            "new_password": self.password,
        }
