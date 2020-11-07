import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog

from uis import settings
from UsefulShit import db, AddToRegistry, DeleteFromRegistry

from Windows.Window import BaseWindow

import sys

# класс для окна настроек
from utils import audio


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

        self.pushButton.clicked.connect(self.convert)
        self.pushButton_2.clicked.connect(self.bassboost)

        # загрузка данных из бд при открытии окна настроек
        with db:
            cursor = db.cursor()
            autoload = cursor.execute('''
                                        SELECT 
                                            autoload 
                                        FROM 
                                            settings
                                                        ''').fetchone()[0]
            self.language = cursor.execute('''
                                    SELECT 
                                        language 
                                    FROM 
                                        settings
                                                    ''').fetchone()[0]
            self.translate(self.language)

        # изменение radiobuttons в зависимости от значений из бд
        if autoload:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
        else:
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)
        if self.language == 'eng':
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        elif self.language == 'rus':
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

            self.musicopen.setText('Open folder with music')
            self.musicopen.setToolTip('This button opens folder with music')

            self.pushButton.setText('Convert all to wav')
            self.pushButton.setToolTip('This button will convert all your files from music folder '
                                       'to wav.\nYOU WILL LOSE ALL UR ORIGINAL FILES!!!')

            self.pushButton_2.setText('Bassboost all tracks.')
            self.pushButton.setToolTip(
                'This button will bassboost all your tracks from music folder.'
                '\nYOU WILL LOSE ALL UR ORIGINAL FILES!!!')

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

            self.musicopen.setText('Открыть папку с музыкой')
            self.musicopen.setToolTip('Эта кнопка открывает папку с музыкой')

            self.pushButton.setText('Конвертировать в wav')
            self.pushButton.setToolTip('Эта кнопка сконвертирует все ваши файлы из папки с музыкой '
                                       'в wav.\nВЫ ПОТЕРЯЕТЕ ВСЕ ОРИГИНАЛЬНЫЕ ФАЙЛЫ!!!')

            self.pushButton_2.setText('Забассбустить все треки.')
            self.pushButton.setToolTip(
                'Эта кнопка забассбустит все ваши треки из папки с музыкой.'
                '\nВЫ ПОТЕРЯЕТЕ ВСЕ ОРИГИНАЛЬНЫЕ ФАЙЛЫ!!!')

            # имя окна
            self.setWindowTitle('Настройки')

    def bassboost(self):
        audio.bassboost("files/music/")

    def convert(self):
        audio.convertAll("files/music/")

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
