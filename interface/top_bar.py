from tkinter import Menu, Tk


class TopBar(Menu):
    def __init__(self, master: Tk):
        Menu.__init__(self, master)
        self.master = master
        self.info = Menu(self)
        self.edit = Menu(self)
        self.init_menu()

    def init_menu(self):
        self.info.add_command(label='Exit', command=self.master.destroy)
        self.add_cascade(label='Info', menu=self.info)

