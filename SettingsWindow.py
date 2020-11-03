import os

from PyQt5 import QtGui

import settings
from connects import db

from Window import BaseWindow

import getpass


def add_to_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % getpass.getuser()
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" %s' % file_path)


def delete_from_startup(file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % getpass.getuser()
    with open(bat_path + '\\' + "open.bat", "w") as bat_file, open(bat_path + '\\' + "open.bat", "r") as read_bat_file:
        a = read_bat_file.readlines()
        for i, smth in enumerate(a):
            if r'start "" %s' % file_path in smth:
                del a[i]
                return
        bat_file.write(''.join(a))


class SettingsWindow(settings.Ui_MainWindow, BaseWindow):
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
                add_to_startup()

            elif self.sender().text() == 'No':
                cursor.execute('UPDATE settings SET autoload = 0')
                delete_from_startup()

    def sql_language(self):
        with db:
            lng = self.sender().text()
            cursor = db.cursor()
            cursor.execute(f'UPDATE settings SET language = "{lng}"')
            self.parent.language = lng

        self.translate(lng)

    def translate(self, lang):
        if lang == 'eng':
            self.radioButton_3.setToolTip('Tick this if you want this program to load w/ OS')
            self.radioButton_4.setToolTip('Tick this if you dont want this program to load w/ OS')
            self.radioButton.setToolTip(
                'Tick this if you want to see this program on English language')
            self.radioButton_2.setToolTip(
                'Tick this if you want to see this program on Russian language')

            self.label_2.setText('Autoload')
            self.label.setText('Language')

            self.setWindowTitle('Settings')

        elif lang == 'rus':
            self.radioButton_3.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа загружалась вместе с ОС')
            self.radioButton_4.setToolTip(
                'Отметьте это, если вы не хотите, чтобы эта программа загружалась вместе с ОС')
            self.radioButton.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на пендосском языке')
            self.radioButton_2.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на великом и могучем языке')

            self.label_2.setText('Автозагрузка')
            self.label.setText('Язык')

            self.setWindowTitle('Настройки')

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with db:
            cursor = db.cursor()
            lang = cursor.execute('SELECT language FROM settings').fetchone()[0]
        self.parent.translate(lang)
