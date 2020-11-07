import sqlite3
from winreg import *

from PyQt5 import QtCore

import datetime as dt


# подключение к базе данных
db = sqlite3.connect('files/settings.db')


# добавить в реестр
def AddToRegistry(filename):
    # Путь в реестре
    autorun = OpenKey(HKEY_CURRENT_USER,
                     r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                     0, KEY_ALL_ACCESS)
    # Добавить скрипт в автозагрузку
    SetValueEx(autorun, 'bigboy', 0, REG_SZ, filename)
    # Закрыть реестр
    CloseKey(autorun)


# удалить из реестра
def DeleteFromRegistry():
    # Путь в реестре
    autorun = OpenKey(HKEY_CURRENT_USER,
                     r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                     0, KEY_ALL_ACCESS)
    # Удалить скрипт из автозагрузки
    DeleteValue(autorun, 'bigboy')
    # Закрыть реестр
    CloseKey(autorun)


class BrowserHandler(QtCore.QObject):
    running = False
    alarmsignal = QtCore.pyqtSignal(str, str)

    # метод, который будет выполнять алгоритм в другом потоке
    def run(self):
        while True:
            with sqlite3.connect('files/mydb.db') as database:
                cursor = database.cursor()
                # посылаем сигнал из второго потока в GUI поток
                for event in cursor.execute('''
                                            SELECT
                                                * 
                                            FROM 
                                                events
                                            ''').fetchall():
                    # преобразование полученной из бд даты
                    # к формату библиотеки datetime для сравнения
                    event_date_list = str(event[-2]).split('.')
                    event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                                         int(event_date_list[0]))

                    event_time = str(event[-1]).split(':')
                    # срабатывание будильника если время подходит
                    if event_date == dt.date.today():
                        current_time = dt.datetime.now().time()
                        alarm_time = dt.time(hour=int(event_time[0]), minute=int(event_time[1]))

                        if (alarm_time.hour, alarm_time.minute) == \
                                (current_time.hour, current_time.minute):
                            # отправка сигнала с событием в основной поток
                            self.alarmsignal.emit(event[1], ':'.join(event_time))
                            # отдых в 60 секунд, чтобы не открывались новые окна)
                            QtCore.QThread.sleep(60)
