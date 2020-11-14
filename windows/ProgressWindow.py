from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QDialog, Qt
from PyQt5.QtGui import QIcon

from uis import progress
from utils.other import *


class ProgressWindow(QDialog, progress.Ui_Dialog):

    def __init__(self, mainWindow, label):
        super().__init__()
        self.mainWindow = mainWindow
        self.setWindowIcon(QIcon(f'{iconsdir}/jojo.ico'))
        self.setupUi(self)
        self.label.setText(label)
        self.translate(mainWindow.language)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint & ~Qt.WindowCloseButtonHint);

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
    
    
    @QtCore.pyqtSlot()
    def emptyCallback(self):
        if self.mainWindow.language == 'rus':
            QtWidgets.QMessageBox.warning(self, 'Внимание', "Папка пуста", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', "Empty folder" , QtWidgets.QMessageBox.Ok)
        self.close()
    
    @QtCore.pyqtSlot()
    def AllMP3Callback(self):
        if self.mainWindow.language == 'rus':
            QtWidgets.QMessageBox.warning(self, 'Внимание', "Нечего конвертировать", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', "Nothing to convert" , QtWidgets.QMessageBox.Ok)
        self.close()
    
    @QtCore.pyqtSlot(str, Exception)
    def errCallback(self, file, e):
        if self.mainWindow.language == 'rus':
            QtWidgets.QMessageBox.critical(self, 'Произошла ошибка', f"Ошибка при обработке {file}:\n" + str(e), QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.critical(self, 'Error', f"Error while processing {file}:\n" + str(e), QtWidgets.QMessageBox.Ok)
        self.close()
