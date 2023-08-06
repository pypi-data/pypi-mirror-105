class TestAR:
    def __init__(self, ar_status='Готов'):
        self.ar_status = ar_status

    def get_api_support_methods(self):
        methods = {'get_status': {'method': self.get_status}}
        return methods

    def get_status(self):
        return self.ar_status
