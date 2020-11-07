import datetime

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from Windows.Window import BaseWindow
from uis import addevent
from utils.other import *


# класс для окна с добавлением нового события
class AddEventWindow(BaseWindow, addevent.Ui_MainWindow):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.pushButton.clicked.connect(self.additem)

        self.dateEdit.setMinimumDate(datetime.date.today())
        self.timeEdit.setMinimumTime(datetime.datetime.now().time())

        self.translate(self.mainWindow.language)

    def additem(self):  # добавление нового значения в таблицу и обновление базы данных
        name = self.lineEdit.text()
        if name:
            self.mainWindow.tableWidget.setRowCount(self.mainWindow.tableWidget.rowCount() + 1)
            self.mainWindow.tableWidget.setItem(self.mainWindow.tableWidget.rowCount() - 1, 0, QTableWidgetItem(name))
            self.mainWindow.tableWidget.setItem(self.mainWindow.tableWidget.rowCount() - 1, 1,
                                            QTableWidgetItem(self.dateEdit.text()))
            self.mainWindow.tableWidget.setItem(self.mainWindow.tableWidget.rowCount() - 1, 2,
                                            QTableWidgetItem(self.timeEdit.text()))
            self.mainWindow.update_db()
            self.close()
        else:
            if self.mainWindow.language == 'eng':
                self.message = QMessageBox.warning(self, 'Warning', 'Please input name of ur event',
                                                   QMessageBox.Cancel)
            elif self.mainWindow.language == 'rus':
                self.message = QMessageBox.warning(self, 'Предупреждение',
                                                   'Пожалуйста, введите название для вашего события',
                                                   QMessageBox.Cancel)

    def translate(self, lang):  # перевод окна с добавлением нового события
        if lang == 'eng':
            self.label_2.setText('Event name')
            self.label_3.setText('Date')
            self.label.setText('Time')
            self.pushButton.setText('Add event')

            self.lineEdit.setToolTip('Write here ur event\'s name')
            self.timeEdit.setToolTip('Choose date and time of ur event')
            self.pushButton.setToolTip('Press this button to add this event')

            self.setWindowTitle('Add new event')
        elif lang == 'rus':
            self.label_2.setText('Название события')
            self.label_3.setText('Дата')
            self.label.setText('Время')
            self.pushButton.setText('Добавить событие')

            self.lineEdit.setToolTip('Напишите здесь название вашего события')
            self.timeEdit.setToolTip('Выберите дату и время вашего события')
            self.pushButton.setToolTip('Нажмите эту кнопку, чтобы добавить новое событие')

            self.setWindowTitle('Добавить новое событие')

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Enter - 1:  # добавление элементов в таблицу с помощью кнопки ENTER
            self.additem()
