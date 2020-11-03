import sqlite3
import time
import datetime as dt

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem

import design
from connects import db

from AddEventWindow import AddEventWindow
from SettingsWindow import SettingsWindow
from Window import BaseWindow

from threading import Thread


# функция для сортировки событий по дате и времени
def sort_by_datetime(smth):
    return smth[2], smth[3], smth[1][0]


# класс главного окна
class MyMainWindow(design.Ui_mainWindow, BaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.addEvent.clicked.connect(self.add_event)
        self.deleteEvent.clicked.connect(self.delete_event)
        self.settingsButton.clicked.connect(self.open_settings)

        # загрузка данных из бд при запуске программы
        with db:
            cursor = db.cursor()
            # получение языка программы из бд и ее перевод
            self.language = cursor.execute('SELECT language FROM settings').fetchone()[0]
            self.translate(self.language)

            # получение данных о будильниках и добавление их в TableWidget
            data = cursor.execute('SELECT name, date, time FROM events').fetchall()
            self.tableWidget.setRowCount(len(data))
            for i, frag in enumerate(data):
                for j, elem in enumerate(frag):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        # создание потока на проверку времени для будильников
        self.thread = Thread(target=self.check_time)
        self.thread.start()
        self.stop_thread = False

    # функция для потока на проверку времени для будильников
    def check_time(self):
        db = sqlite3.connect('mydb.db')
        while not self.stop_thread:
            cursor = db.cursor()
            for event in cursor.execute('SELECT * FROM events').fetchall():
                # преобразование полученной из бд даты к формату библиотеки datetime для сравнения
                event_date_list = str(event[-2]).split('.')
                event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                                     int(event_date_list[0]))

                event_time = event[-1]
                # срабатывание будильника если время подходит
                if event_date == dt.date.today():
                    current_time = dt.datetime.now().time()
                    if str(
                            event_time) == f'{current_time.hour}:{current_time.minute}':
                        self.alarm(event[0])
                        time.sleep(60)
            time.sleep(1)
        return

    # срабатывание будильника
    def alarm(self, name):
        pass

    # перевод главного окна
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

    # открытие окна с добавлением нового события
    def add_event(self):
        self.addevent = AddEventWindow(self)
        self.addevent.show()

    # открытие окна с удалением выбранного события
    def delete_event(self):
        if self.tableWidget.selectedItems():
            while self.tableWidget.selectedItems():
                self.tableWidget.removeRow(self.tableWidget.selectedItems()[0].row())
            self.update_db()
        else:
            if self.language == 'eng':
                self.message = QMessageBox.warning(self, 'Warning',
                                                   'Please choose events to delete',
                                                   QMessageBox.Cancel)
            elif self.language == 'rus':
                self.message = QMessageBox.warning(self, 'Предупреждение',
                                                   'Пожалуйста, выберите события для удаления',
                                                   QMessageBox.Cancel)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:

        # Удаление элементов из таблицы с помощью кнопки DEL
        if event.key() == Qt.Key_Delete:
            self.delete_event()

    def open_settings(self):
        self.settings = SettingsWindow(self)
        self.settings.show()

    def update_db(self):
        # создаем список из ивентов, чтобы его нормально отсортировать, заливаем его в tablewidget
        events = []
        for i in range(self.tableWidget.rowCount()):
            items = [str(i + 1)]
            for j in range(self.tableWidget.columnCount()):
                items.append(str(self.tableWidget.item(i, j).text()))
            events.append(items)
        events.sort(key=sort_by_datetime)
        # заливаем отсортированный список в бд
        with db:
            cursor = db.cursor()
            cursor.execute('DELETE FROM events')
            for i, column in enumerate(events):
                cursor.execute('INSERT INTO events(number, name, date, time) VALUES(?, ?, ?, ?)',
                               tuple(column))
                for j, elem in enumerate(column[1::]):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    # close event и закрытие thread на срабатывание таймера
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.stop_thread = True
