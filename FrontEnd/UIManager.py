from FrontEnd.UIControl.FirstStage import FirstStage
from FrontEnd.UIControl.UIMainWindow import UIMainWindow


class UIManager:
    def __init__(self):
        self.active_window = None
        self.list_of_windows = [FirstStage(self)]  # Sequence of windows to show
        self.window_iterator = -1

    def begin(self):
        """
        Shows the first window (Main Window)
        """
        self.active_window = UIMainWindow(self)
        self.active_window.show()

    def next_window(self):
        """
        Closes the current active window and shows the next one from the window sequence.
        """
        if len(self.list_of_windows) > self.window_iterator + 1:
            self.active_window.close()
            self.window_iterator += 1
            self.active_window = self.list_of_windows[self.window_iterator]
            self.active_window.start()

    def previous_window(self):
        """
        Closes the current active window and shows the previous one from the window sequence.
        """
        if self.window_iterator > 0:
            self.active_window.close()
            self.window_iterator -= 1
            self.active_window = self.list_of_windows[self.window_iterator]
            self.active_window.start()
