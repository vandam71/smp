from tkinter import Tk
from tkinter.ttk import Notebook
from interface.top_bar import TopBar
from interface.tab import Tab


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.master_tab = Notebook(self)
        self.title('Stock Market Predictor')
        self.geometry("640x480")
        self.tabs = {}
        top_bar = TopBar(self)
        self.config(menu=top_bar)
        self.init_application()

    def init_application(self):
        for tab in self.tabs:
            self.master_tab.add(tab, text=tab.name)
        self.master_tab.pack(expand=1, fill='both')

    def add_tab(self, tab):
        self.master_tab.add(tab, text=tab.name)
        self.master_tab.pack(expand=1, fill='both')
