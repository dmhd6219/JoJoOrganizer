import datetime

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from windows.Window import BaseWindow
from uis import addevent
from utils.errors import EmptyTitle, TimeError, DateError, DateTimeError
from utils.other import *


# класс для окна с добавлением нового события
class AddEventWindow(BaseWindow, addevent.Ui_MainWindow):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.pushButton.clicked.connect(self.additem)

        self.dateEdit.setMinimumDate(datetime.date.today())
        self.timeEdit.setMinimumTime(datetime.datetime.now().time())

        self.dateEdit.dateChanged.connect(self.change_date)

        self.translate(self.mainWindow.language)

    def change_date(self):
        event_date_list = self.dateEdit.text().split('.')
        event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                             int(event_date_list[0]))
        # проверка, является ли указанная дата будущей
        if event_date > dt.date.today():
            self.timeEdit.setMinimumTime(datetime.time(hour=0, minute=0))
        else:
            self.timeEdit.setMinimumTime(dt.datetime.now().time())

    # добавление нового значения в таблицу и обновление базы данных
    def additem(self):
        try:
            name = self.lineEdit.text().strip()
            # проверка, введено ли время
            if not name:
                if self.mainWindow.language == 'eng':
                    raise EmptyTitle('Please input name of ur event')

                elif self.mainWindow.language == 'rus':
                    raise EmptyTitle('Пожалуйста, введите название для вашего события')

            event_time = self.timeEdit.text().split(':')
            alarm_time = dt.time(hour=int(event_time[0]), minute=int(event_time[1]))
            current_time = dt.datetime.now().time()
            event_date_list = self.dateEdit.text().split('.')
            event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                                 int(event_date_list[0]))

            # проверка, является ли указанное время прошедшим
            if (alarm_time.hour, alarm_time.minute) < (current_time.hour, current_time.minute) and \
                    event_date == dt.date.today():
                if self.mainWindow.language == 'rus':
                    raise TimeError('Указанное время меньше текущего')
                raise TimeError('Written time is less than current')

            # проверка, является ли указанная дата прошедшей
            if event_date < dt.date.today():
                if self.mainWindow.language == 'rus':
                    raise DateError('Указанная дата меньше текущей')
                raise DateError('Written date is less than current')

            with db:
                cursor = db.cursor()
                data = cursor.execute('SELECT date, time FROM events').fetchall()
                for i in data:
                    if self.dateEdit.text() == i[0] and self.timeEdit.text() == i[1]:
                        if self.mainWindow.language == 'rus':
                            raise DateTimeError('Событие с такой датой и временем уже существует')
                        raise DateTimeError('Event with this date and time already exists')

            # добавление события в таблицу
            self.mainWindow.tableWidget.setRowCount(self.mainWindow.tableWidget.rowCount() + 1)
            self.mainWindow.tableWidget.setItem(self.mainWindow.tableWidget.rowCount() - 1, 0,
                                                QTableWidgetItem(name))
            self.mainWindow.tableWidget.setItem(self.mainWindow.tableWidget.rowCount() - 1, 1,
                                                QTableWidgetItem(self.dateEdit.text()))
            self.mainWindow.tableWidget.setItem(self.mainWindow.tableWidget.rowCount() - 1, 2,
                                                QTableWidgetItem(self.timeEdit.text()))
            # обновление базы данных
            self.mainWindow.update_db()
            # закрытие окна
            self.close()

        except Exception as ex:
            if self.mainWindow.language == 'rus':
                self.message = QMessageBox.warning(self, 'Предупреждение',
                                                   str(ex), QMessageBox.Cancel)
            else:
                self.message = QMessageBox.warning(self, 'Warning', str(ex), QMessageBox.Cancel)

    # перевод окна с добавлением нового события
    def translate(self, lang):
        if lang == 'eng':
            self.label_2.setText('Event name')
            self.label_3.setText('Date')
            self.label.setText('Time')
            self.pushButton.setText('Add event')

            self.lineEdit.setToolTip('Write here ur event\'s name')
            self.timeEdit.setToolTip('Choose date and time of ur event')
            self.pushButton.setToolTip('Press this button to add this event')

            self.setWindowTitle('Add new event')
        elif lang == 'rus':
            self.label_2.setText('Название события')
            self.label_3.setText('Дата')
            self.label.setText('Время')
            self.pushButton.setText('Добавить событие')

            self.lineEdit.setToolTip('Напишите здесь название вашего события')
            self.timeEdit.setToolTip('Выберите дату и время вашего события')
            self.pushButton.setToolTip('Нажмите эту кнопку, чтобы добавить новое событие')

            self.setWindowTitle('Добавить новое событие')

    # добавление элементов в таблицу с помощью кнопки ENTER
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_Enter - 1:
            self.additem()
