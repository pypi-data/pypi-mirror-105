class RequestError(Exception):
    def __init__(self, *, message=None, response=None):            self.status = getattr(response, "status", None)
        self.message = message or (f"Retrieved a response with the status code of {self.status}." if self.status else None)
        super().__init__(self.message)                     
    def __str__(self):
        return self.message

    def __repr__(self):
        return f"<RequestError [{self.status or self.message}]>"
