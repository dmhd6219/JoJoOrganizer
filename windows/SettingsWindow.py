import os
import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from windows.ProgressWindow import ProgressWindow
from windows.Window import BaseWindow
from uis import settings
from utils import audio
from utils.other import *


class SettingsWindow(BaseWindow, settings.Ui_MainWindow):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setupUi(self)

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
            autoload = cursor.execute('SELECT autoload FROM settings').fetchone()[0]
            self.translate(self.mainWindow.language)

        # изменение radiobuttons в зависимости от значений из бд
        if autoload:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
        else:
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)
        if self.mainWindow.language == 'eng':
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        elif self.mainWindow.language == 'rus':
            self.radioButton_2.setChecked(True)
            self.radioButton.setChecked(False)

    # открытие папки с музыкой
    def open_musicfolder(self):
        os.startfile(f'{cd}/{musicdir}')

    # обновление параметра автозагрузки в бд и в регистре винды
    def sql_autoload(self):
        with db:
            cursor = db.cursor()
            if self.sender().text() == 'Ya':
                fname = ''
                if getattr(sys, 'frozen', False):  # если запускается exe файл
                    fname = sys.executable.replace('/', '\\')
                elif __file__:  # если запускается py файл
                    fname = (self.mainWindow.file.replace('/', '\\'))

                if fname:
                    cursor.execute('UPDATE settings SET autoload = 1')
                    AddToRegistry(fname)
                else:
                    self.radioButton_4.setChecked(True)

            elif self.sender().text() == 'No':
                autoload = cursor.execute('SELECT autoload FROM settings').fetchone()[0]
                if autoload:
                    cursor.execute('UPDATE settings SET autoload = 0')
                    DeleteFromRegistry()

    # обновление языка программы в базе данных
    def sql_language(self):
        with db:
            self.mainWindow.language = self.sender().text()
            cursor = db.cursor()
            cursor.execute(f'UPDATE settings SET language = "{self.mainWindow.language}"')

        self.translate(self.mainWindow.language)

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

            self.pushButton_2.setText('Auto-Bassboost')
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

            self.pushButton_2.setText('Авто-бассбуст')
            self.pushButton.setToolTip(
                'Эта кнопка забассбустит все ваши треки из папки с музыкой.'
                '\nВЫ ПОТЕРЯЕТЕ ВСЕ ОРИГИНАЛЬНЫЕ ФАЙЛЫ!!!')

            # имя окна
            self.setWindowTitle('Настройки')

    def startTaskNewThread(self, window):
        window.show()
        if isinstance(self.thread, QtCore.QThread):
            self.thread.exit()
            self.thread.wait()

        self.thread = QtCore.QThread()
        self.thread.setTerminationEnabled(True)
        self.worker.moveToThread(self.thread)
        self.worker.setProgress.connect(window.setProgress)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
    
    # бассбуст)
    def bassboost(self):
        if self.mainWindow.language == 'rus':
            self.message = QMessageBox.question(self, 'Предупреждение',
                                                "Продолжить? Все ваши оригинальные треки будут потеряны",
                                                QMessageBox.Yes | QMessageBox.Cancel,
                                                QMessageBox.Yes)
        else:
            self.message = QMessageBox.question(self, 'Warning',
                                                "Proceed? All your original tracks will be lost",
                                                QMessageBox.Yes | QMessageBox.Cancel,
                                                QMessageBox.Yes)
        if self.message == QMessageBox.Yes:
            if self.mainWindow.language == "rus":
                label = "Прибавляем децибелы.."
            else:
                label = "Adding decibels.."
            self.window = ProgressWindow(self.mainWindow, label)
            self.worker = audio.Bassbooster()
            self.startTaskNewThread(self.window)

    # конвертация треков в wav
    def convert(self):
        if self.mainWindow.language == 'rus':
            self.message = QMessageBox.question(self, 'Предупреждение',
                                                "Продолжить? Все ваши оригинальные треки будут потеряны",
                                                QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)
        else:
            self.message = QMessageBox.question(self, 'Warning',
                                                "Proceed? All your original tracks will be lost",
                                                QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)
        if self.message == QMessageBox.Yes:
            if self.mainWindow.language == "rus":
                label = "Конвертирование.."
            else:
                label = "Converting.."
            self.window = ProgressWindow(self.mainWindow, label)
            self.worker = audio.Converter()
            self.startTaskNewThread(self.window)

    # обнеовление языка основного окна при закрытии этого
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with db:
            cursor = db.cursor()
            self.mainWindow.language = cursor.execute('SELECT language FROM settings').fetchone()[0]
        self.mainWindow.translate(self.mainWindow.language)
