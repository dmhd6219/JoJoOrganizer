import sqlite3
import sys
import random

from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

import design
import settings
import addevent

db = sqlite3.connect('mydb.db')


class AddEventWindow(addevent.Ui_MainWindow, QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.pushButton.clicked.connect(self.additem)
        with db:
            cursor = db.cursor()
            lang = cursor.execute('SELECT language FROM settings').fetchone()[0]
            self.translate = self.translate(lang)

    def additem(self):
        self.parent.tableWidget.setRowCount(self.parent.tableWidget.rowCount() + 1)
        self.parent.tableWidget.setItem(self.parent.tableWidget.rowCount() - 1, 0,
                                        QTableWidgetItem(self.lineEdit.text()))
        self.parent.tableWidget.setItem(self.parent.tableWidget.rowCount() - 1, 1,
                                        QTableWidgetItem(self.dateEdit.text()))
        self.parent.tableWidget.setItem(self.parent.tableWidget.rowCount() - 1, 2,
                                        QTableWidgetItem(self.timeEdit.text()))
        self.parent.update_db()
        self.close()

    def translate(self, lang):
        if lang == 'eng':
            self.label_2.setText('Event name')
            self.label.setText('Date')
            self.label_3.setText('Time')
            self.pushButton.setText('Add event')

            self.lineEdit.setToolTip('Write here ur event\'s name')
            self.timeEdit.setToolTip('Choose date and time of ur event')
            self.pushButton.setToolTip('Press this button to add this event')

        elif lang == 'rus':
            self.label_2.setText('Название события')
            self.label.setText('Дата')
            self.label_3.setText('Время')
            self.pushButton.setText('Добавить событие')

            self.lineEdit.setToolTip('Напишите здесь название вашего события')
            self.timeEdit.setToolTip('Выберите дату и время вашего события')
            self.pushButton.setToolTip('Нажмите эту кнопку, чтобы добавить новое событие')


class SettingsWindow(settings.Ui_MainWindow, QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        [x.clicked.connect(self.sql_autoload) for x in self.autoload_group.buttons()]
        [x.clicked.connect(self.sql_language) for x in self.language_group.buttons()]

        with db:
            cursor = db.cursor()
            autoload = cursor.execute('SELECT autoload FROM settings').fetchone()[0]
            lang = cursor.execute('SELECT language FROM settings').fetchone()[0]
            self.translate = self.translate(lang)

        if autoload:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
        else:
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)

        if lang == 'eng':
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        elif lang == 'rus':
            self.radioButton_2.setChecked(True)
            self.radioButton.setChecked(False)

    def sql_autoload(self):
        with db:
            cursor = db.cursor()
            if self.sender().text() == 'Ya':
                cursor.execute('UPDATE settings SET autoload = 1')
            elif self.sender().text() == 'No':
                cursor.execute('UPDATE settings SET autoload = 0')

    def sql_language(self):
        with db:
            cursor = db.cursor()
            if self.sender().text() == 'Eng':
                cursor.execute('UPDATE settings SET language = "eng"')
            elif self.sender().text() == 'Rus':
                cursor.execute('UPDATE settings SET language = "rus"')

    def translate(self, lang):
        if lang == 'eng':
            self.radioButton_3.setToolTip('Tick this if you want this program to load w/ OS')
            self.radioButton_4.setToolTip('Tick this if you dont want this program to load w/ OS')
            self.radioButton.setToolTip(
                'Tick this if you want to see this program on English language')
            self.radioButton_2.setToolTip(
                'Tick this if you want to see this program on Russian language')

            self.label.setText('Autoload')
            self.label_2.setText('Language')

        elif lang == 'rus':
            self.radioButton_3.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа загружалась вместе с ОС')
            self.radioButton_4.setToolTip(
                'Отметьте это, если вы не хотите, чтобы эта программа загружалась вместе с ОС')
            self.radioButton.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на пендосском языке')
            self.radioButton_2.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на великом и могучем языке')

            self.label.setText('Автозагрузка')
            self.label_2.setText('Язык')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with db:
            cursor = db.cursor()
            lang = cursor.execute('SELECT language FROM settings').fetchone()[0]
        self.parent.translate(lang)


class DBSample(design.Ui_mainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.addEvent.clicked.connect(self.add_event)
        self.deleteEvent.clicked.connect(self.delete_event)
        self.settingsButton.clicked.connect(self.open_settings)

        with db:
            cursor = db.cursor()
            self.language = cursor.execute('SELECT language FROM settings').fetchone()[0]
            self.translate(self.language)

            data = cursor.execute('SELECT name, date, time FROM events').fetchall()
            self.tableWidget.setRowCount(len(data))
            for i, frag in enumerate(data):
                for j, elem in enumerate(frag):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    def translate(self, lang):
        if lang == 'eng':
            self.tableWidget.setHorizontalHeaderLabels(['Event', 'Data', 'Time'])
            self.tableWidget.setToolTip('Here you can see your events')

            self.addEvent.setText('Add event')
            self.addEvent.setToolTip('This button adds new event')

            self.deleteEvent.setText('Delete selected events')
            self.deleteEvent.setToolTip('This button deletes selected events')

            self.settingsButton.setToolTip('This button opens settings menu')

        elif lang == 'rus':
            self.tableWidget.setHorizontalHeaderLabels(['Событие', "Дата", "Время"])
            self.tableWidget.setToolTip('Тут вы можете увидеть ваши события')

            self.addEvent.setText('Новое событие')
            self.addEvent.setToolTip('Эта кнопка добавляет новое событие')

            self.deleteEvent.setText('Удалить событие')
            self.deleteEvent.setToolTip('Эта кнопка удаляет событие')

            self.settingsButton.setToolTip('Эта кнопка открывает меню настроек')

    def add_event(self):
        self.addevent = AddEventWindow(self)
        self.addevent.show()

    def delete_event(self):
        if self.tableWidget.selectedItems():
            while self.tableWidget.selectedItems():
                self.tableWidget.removeRow(self.tableWidget.selectedItems()[0].row())
            self.update_db()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:

        # Удаление элементов из таблицы с помощью кнопки DEL
        if event.key() == Qt.Key_Delete:
            self.delete_event()

    def open_settings(self):
        self.settings = SettingsWindow(self)
        self.settings.show()

    def update_db(self):
        self.tableWidget.sortByColumn(1, QtCore.Qt.AscendingOrder)
        with db:
            cursor = db.cursor()
            cursor.execute('DELETE FROM events')
            for i in range(self.tableWidget.rowCount()):
                items = [str(i + 1)]
                for j in range(self.tableWidget.columnCount()):
                    items.append(str(self.tableWidget.item(i, j).text()))
                cursor.execute('INSERT INTO events(number, name, date, time) VALUES(?, ?, ?, ?)',
                               tuple(items))


def exception_hook(exctype, value, traceback):
    sys.excepthook(exctype, value, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
