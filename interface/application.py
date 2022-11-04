from tkinter import Tk, Button
from tkinter.ttk import Notebook
from interface.top_bar import TopBar


class Application(Tk):
    SIZE = "1280x720"

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.master_tab = Notebook(self)
        self.title('Stock Market Predictor')
        self.geometry(self.SIZE)
        self.tabs = {}
        top_bar = TopBar(self)
        self.config(menu=top_bar)
        self.init_application()

    def init_application(self):
        for tab in self.tabs:
            self.master_tab.add(tab, text=tab.name)
        self.master_tab.pack(expand=1, fill='both')

    def add_tab(self, tab):
        del_button = Button(tab, text='Delete', command=self.delete_tab)
        del_button.pack()
        self.master_tab.add(tab, text=tab.name)
        self.master_tab.pack(expand=1, fill='both')

    def delete_tab(self):
        self.master_tab.forget(self.master_tab.select())
