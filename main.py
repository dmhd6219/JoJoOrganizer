import sqlite3
import sys
import random

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

import design
import settings

db = sqlite3.connect('mydb.db')


class SettingsWindow(settings.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        [x.clicked.connect(self.sql_autoload) for x in self.autoload_group.buttons()]
        [x.clicked.connect(self.sql_language) for x in self.language_group.buttons()]

        with db:
            cursor = db.cursor()
            autoload = cursor.execute('SELECT autoload FROM settings').fetchone()[0]
            lang = cursor.execute('SELECT language FROM settings').fetchone()[0]
            self.translate(lang)

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

    def translate(self, lang):
        if lang == 'eng':
            self.tableWidget.setHorizontalHeaderLabels(['Event', 'Time'])
            self.tableWidget.setToolTip('Here you can see your events')

            self.addEvent.setText('Add event')
            self.addEvent.setToolTip('This button adds new event')

            self.deleteEvent.setText('Delete selected events')
            self.deleteEvent.setToolTip('This button deletes selected events')

            self.settingsButton.setToolTip('This button opens settings menu')

        elif lang == 'rus':
            self.tableWidget.setHorizontalHeaderLabels(['Событие', "Время"])
            self.tableWidget.setToolTip('Тут вы можете увидеть ваши события')

            self.addEvent.setText('Новое событие')
            self.addEvent.setToolTip('Эта кнопка добавляет новое событие')

            self.deleteEvent.setText('Удалить событие')
            self.deleteEvent.setToolTip('Эта кнопка удаляет событие')

            self.settingsButton.setToolTip('Эта кнопка открывает меню настроек')

    def add_event(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 0,
                                 QTableWidgetItem(f'event1{random.randint(0, 666)}'))
        self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(f'66:66'))

    def delete_event(self):
        if self.tableWidget.selectedItems():
            while self.tableWidget.selectedItems():
                self.tableWidget.removeRow(self.tableWidget.selectedItems()[0].row())

    def open_settings(self):
        self.settings = SettingsWindow()
        self.settings.show()
        with db:
            cursor = db.cursor()
            self.language = cursor.execute('SELECT language FROM settings').fetchone()[0]
            print(self.language)
        self.translate(self.language)


def exception_hook(exctype, value, traceback):
    sys.excepthook(exctype, value, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())
