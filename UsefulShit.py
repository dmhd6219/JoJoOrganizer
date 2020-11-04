import sqlite3
from winreg import *

# подключение к базе данных
db = sqlite3.connect('files/mydb.db')


# добавление в регистр
def AddToRegistry(filename):
    # Путь в реестре
    key_my = OpenKey(HKEY_CURRENT_USER,
                     r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                     0, KEY_ALL_ACCESS)
    # Установить скрипт в автозагрузку
    SetValueEx(key_my, 'bigboy', 0, REG_SZ, filename)
    # Закрыть реестр
    CloseKey(key_my)


# удаление из регистра
def DeleteFromRegistry():
    # Путь в реестре
    key_my = OpenKey(HKEY_CURRENT_USER,
                     r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
                     0, KEY_ALL_ACCESS)
    # Установить скрипт в автозагрузку
    DeleteValue(key_my, 'bigboy')
    # Закрыть реестр
    CloseKey(key_my)
