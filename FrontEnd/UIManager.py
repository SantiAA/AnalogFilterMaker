from FrontEnd.UIControl.FirstStage import FirstStage
from FrontEnd.UIControl.UIMainWindow import UIMainWindow


class UIManager:
    def __init__(self):
        self.active_window = None
        self.list_of_windows = [FirstStage(self)]
        self.window_iterator = -1

    def begin(self):
        self.active_window = UIMainWindow(self)
        self.active_window.show()

    def next_window(self):
        self.active_window.close()
        self.window_iterator += 1
        self.active_window = self.list_of_windows[self.window_iterator]
        self.active_window.start()

