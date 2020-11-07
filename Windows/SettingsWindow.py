import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog

from uis import settings
from UsefulShit import db, AddToRegistry, DeleteFromRegistry

from Windows.Window import BaseWindow
from Windows.FAQWindow import FAQWindow

import sys
import pathlib


# класс для окна настроек
class SettingsWindow(settings.Ui_MainWindow, BaseWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent

        # проверка ос
        self.platform = sys.platform
        if 'win' not in self.platform:
            self.radioButton_4.setEnabled(False)
            self.radioButton_3.setEnabled(False)

        [x.clicked.connect(self.sql_autoload) for x in self.autoload_group.buttons()]
        [x.clicked.connect(self.sql_language) for x in self.language_group.buttons()]
        self.musicopen.clicked.connect(self.open_musicfolder)

        # загрузка данных из бд при открытии окна настроек
        with db:
            cursor = db.cursor()
            autoload = cursor.execute('''
                                        SELECT 
                                            autoload 
                                        FROM 
                                            settings
                                                        ''').fetchone()[0]
            lang = cursor.execute('''
                                    SELECT 
                                        language 
                                    FROM 
                                        settings
                                                    ''').fetchone()[0]
            self.translate(lang)

        # изменение radiobuttons в зависимости от значений из бд
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

    # открытие папки с музыкой
    def open_musicfolder(self):
        application_path = ''
        # если запускается exe файл
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        # если запускается py файл
        elif __file__:
            application_path = ''.join(os.path.dirname(__file__).split('\\')[:-1:])
        if application_path:
            os.system(f'start {application_path}/files/music')

    # обновление параметра автозагрузки в бд и в регистре винды
    def sql_autoload(self):
        with db:
            cursor = db.cursor()
            if self.sender().text() == 'Ya':
                fname = QFileDialog.getOpenFileName(
                    self, 'Выберите исполняемый файл с данной программой', '',
                    'Исполняемый файл (*.exe)')[0]

                if fname:
                    cursor.execute('''
                                        UPDATE
                                            settings
                                        SET
                                            autoload = 1
                                                            ''')
                    AddToRegistry(fname)
                else:
                    self.radioButton_4.setChecked(True)

            elif self.sender().text() == 'No':
                autoload = cursor.execute('''
                                                        SELECT 
                                                            autoload 
                                                        FROM 
                                                            settings
                                                                        ''').fetchone()[0]
                if autoload:
                    cursor.execute('''
                           UPDATE
                               settings
                          SET
                               autoload = 0''')
                    DeleteFromRegistry()

    # обновление языка программы в базе данных
    def sql_language(self):
        with db:
            lng = self.sender().text()
            cursor = db.cursor()
            cursor.execute(f'''
                                UPDATE 
                                    settings 
                                SET 
                                    language = "{lng}"
                                                        ''')
            self.parent.language = lng

        self.translate(lng)

    # функция перевода окна
    def translate(self, lang):
        if lang == 'eng':
            # подсказка для параметра автозагрузки, если ос не винда
            if self.platform != 'windows':
                self.radioButton_3.setToolTip(
                    'On ur OS this feature will be available in close future.')
                self.radioButton_4.setToolTip(
                    'On ur OS this feature will be available in close future.')
                self.label_2.setToolTip('On ur OS this feature will be available in close future.')

            # подсказка для параметра языка
            self.radioButton.setToolTip(
                'Tick this if you want to see this program on English language')
            self.radioButton_2.setToolTip(
                'Tick this if you want to see this program on Russian language')

            self.label_2.setText('Autoload')
            self.label.setText('Language')
            self.label_3.setText('Open folder with music')

            self.musicopen.setText('Open folder with music')
            self.musicopen.setToolTip('This button opens folder with music')

            # имя окна
            self.setWindowTitle('Settings')

        elif lang == 'rus':
            # подсказка для параметра автозагрузки, если ос не винда
            if 'win' not in self.platform:
                self.radioButton_3.setToolTip(
                    'На вашей ос эта функция будет доступна в ближайшем будущем.')
                self.radioButton_4.setToolTip(
                    'На вашей ос эта функция будет доступна в ближайшем будущем.')
                self.label_2.setToolTip(
                    'На вашей ос эта функция будет доступна в ближайшем будущем.')

            # подсказка для параметра языка
            self.radioButton.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на пендосском языке')
            self.radioButton_2.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на великом и могучем языке')

            self.label_2.setText('Автозагрузка')
            self.label.setText('Язык')
            self.label_3.setText('Открыть папку с музыкой')

            self.musicopen.setText('Открыть папку с музыкой')
            self.musicopen.setToolTip('Эта кнопка открывает папку с музыкой')

            # имя окна
            self.setWindowTitle('Настройки')

    # обнеовление языка основного окна при закрытии этого
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with db:
            cursor = db.cursor()
            lang = cursor.execute('''
                                    SELECT 
                                        language 
                                    FROM 
                                        settings
                                                    ''').fetchone()[0]
        self.parent.translate(lang)
