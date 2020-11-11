import os, sys
import sqlite3
from winreg import *

from PyQt5 import QtCore

import datetime as dt


def AddToRegistry(filename):  # добавление в реестр
    # Путь в реестре
    autorun = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0,
                      KEY_ALL_ACCESS)
    SetValueEx(autorun, 'bigboy', 0, REG_SZ, filename)  # Добавить скрипт в автозагрузку
    CloseKey(autorun)  # Закрыть реестр


def DeleteFromRegistry():  # удалить из реестра
    # Путь в реестре
    autorun = OpenKey(HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0,
                      KEY_ALL_ACCESS)
    DeleteValue(autorun, 'bigboy')  # Удалить скрипт из автозагрузки
    CloseKey(autorun)  # Закрыть реестр


def resourcePath(relative_path):  # получить абсолютный путь (для  работы pyinstaller)
    path = os.path.abspath(__file__).replace("\\" + __name__.replace(".", "\\") + ".py", "")
    run_path = getattr(sys, '_MEIPASS', path)
    return run_path.replace("\\", "/") + "/" + relative_path


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


iconsdir = resourcePath("files/icons")
texturedir = resourcePath("files/textures")

musicdir = "files/music"
dbfile = "files/settings.db"

cd = ""
if getattr(sys, 'frozen', False):  # если запускается exe файл
    cd = os.path.dirname(sys.executable)
elif __file__:  # если запускается py файл
    cd = '/'.join(os.path.dirname(__file__).split('\\')[:-1:])
            
if not os.path.exists(cd + '/' + musicdir):
    os.makedirs(cd + '/' + musicdir)
    
# подключение к бд
db = sqlite3.connect(cd + '/' + dbfile)
