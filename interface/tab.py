from tkinter import Frame, BOTH, TOP
from abc import ABC, abstractmethod
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class Tab(Frame, ABC):
    def __init__(self, name):
        Frame.__init__(self)
        ABC.__init__(self)
        self.name = name

    @abstractmethod
    def change_content(self, content):
        pass


class GraphWindow(Tab):
    def __init__(self, name):
        Tab.__init__(self, name)

    def change_content(self, content):
        canvas = FigureCanvasTkAgg(content, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
