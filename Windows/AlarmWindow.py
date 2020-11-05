from Windows.Window import BaseWindow
from uis import alarm


class AlarmWindow(alarm.Ui_MainWindow, BaseWindow):
    def __init__(self, title, time):
        super().__init__()
        self.setupUi(self)
        self.title = title
        self.time = time

        self.name.setText(self.title)
        self.time.setText(self.time)

        self.showgl()

    def showgl(self):
        # рандомная опен гл штука
        pass
