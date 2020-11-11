import os
import sqlite3
import sys
from winreg import *

from PyQt5 import QtCore

import datetime as dt

iconsdir = "files/icons"
musicdir = "files/music"
texturedir = "files/textures"

dbfile = "files/settings.db"

application_path = ''


if getattr(sys, 'frozen', False):  # если запускается exe файл
    application_path = os.path.dirname(sys.executable)
elif __file__:  # если запускается py файл
    application_path = '/'.join(os.path.dirname(__file__).split('\\')[:-1:])
# подключение к бд
db = sqlite3.connect(dbfile)


def AddToRegistry(filename):  # добавление в реестр
    application = ''

    if getattr(sys, 'frozen', False):  # если запускается exe файл
        application = sys.executable
    elif __file__:  # если запускается py файл
        application = filename

    print(application)
    # Путь в реестре
    autorun = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0,
                      KEY_ALL_ACCESS)
    SetValueEx(autorun, 'bigboy', 0, REG_SZ, application)  # Добавить скрипт в автозагрузку
    CloseKey(autorun)  # Закрыть реестр


def DeleteFromRegistry():  # удалить из реестра
    # Путь в реестре
    autorun = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0,
                      KEY_ALL_ACCESS)
    DeleteValue(autorun, 'bigboy')  # Удалить скрипт из автозагрузки
    CloseKey(autorun)  # Закрыть реестр


class BrowserHandler(QtCore.QObject):
    running = False
    alarmsignal = QtCore.pyqtSignal(str, str)

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        while True:
            with sqlite3.connect(dbfile) as database:
                cursor = database.cursor()
                # посылаем сигнал из второго потока в поток GUI
                for event in cursor.execute(' SELECT * FROM events').fetchall():
                    # преобразование полученной из бд даты
                    # к формату библиотеки datetime для сравнения
                    event_date_list = str(event[-2]).split('.')
                    event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                                         int(event_date_list[0]))
                    event_time = str(event[-1]).split(':')

                    if event_date == dt.date.today():  # если время подходит, срабатывает будильник
                        current_time = dt.datetime.now().time()
                        alarm_time = dt.time(hour=int(event_time[0]), minute=int(event_time[1]))

                        if (alarm_time.hour, alarm_time.minute) == (
                                current_time.hour, current_time.minute):
                            # отправка сигнала с событием в основной поток
                            self.alarmsignal.emit(event[1], ':'.join(event_time))
                            # отдых в 60 секунд, чтобы не открывались новые окна)
                            QtCore.QThread.sleep(60)
