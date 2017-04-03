from flask_login import *

class SessionUser(UserMixin):
    def __init__(self):
        self.id = "yolo"

    def __init__(self, id):
        self.id = id