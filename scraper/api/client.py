class ApiClient:

    def __init__(self) -> None:
        self.avtogit = Avtogit()
        self.emex = Emex()


class Avtogit:

    def send_orders(self):
        pass


class Emex:

    def get_orders(self):
        pass


client = ApiClient()
