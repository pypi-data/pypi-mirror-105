from time import gmtime, strftime

class TransactionLog:
    def __init__(self, activity, amount):
        self.date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.action = (activity, amount)