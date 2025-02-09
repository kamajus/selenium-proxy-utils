class BrowserNotSupported(Exception):
    def __init__(self):
        super().__init__("This browser is not supported yet.")
