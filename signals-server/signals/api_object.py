from uuid import uuid4

class ApiObject:
    def __init__(self):
        self.id = str(uuid4())
