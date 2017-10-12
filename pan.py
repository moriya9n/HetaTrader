import win32com.client

class ActiveMarket:
    def __init__(self):
        self.prices = win32com.client.Dispatch('ActiveMarket.Prices')
        self.names = win32com.client.Dispatch('ActiveMarket.Names')
        self.calendar = win32com.client.Dispatch('ActiveMarket.Calendar')




