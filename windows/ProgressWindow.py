from PyQt5 import QtCore
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
            self.setWindowTitle('Работаем...')
        elif lang == 'eng':
            self.setWindowTitle('Working...')

    @QtCore.pyqtSlot(int)
    def setProgress(self, percentage):
        if (percentage >= 100):
            self.close()
        self.progressBar.setValue(percentage)