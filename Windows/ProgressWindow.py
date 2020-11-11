from PyQt5.Qt import QDialog, Qt
from PyQt5.QtGui import QIcon

from uis import progress
from utils.other import *


class ProgressWindow(QDialog, progress.Ui_Dialog):

    def __init__(self, mainWindow, label):
        super().__init__()
        self.setWindowIcon(QIcon(f'{iconsdir}/jojo.ico'))
        self.setupUi(self)
        self.label.setText(label)
        self.translate(mainWindow.language)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint);


    # функция перевода
    def translate(self, lang):
        if lang == 'rus':
            self.setWindowTitle('Пожалуйста подождите')
        elif lang == 'eng':
            self.setWindowTitle('Please wait')

    def setProgress(self, percentage):
        self.progressBar.setValue(percentage)
