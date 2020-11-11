import sqlite3

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from Windows.AddEventWindow import AddEventWindow
from Windows.AlarmWindow import AlarmWindow
from Windows.FAQWindow import FAQWindow
from Windows.SettingsWindow import SettingsWindow
from Windows.Window import BaseWindow
import datetime as dt
from uis import design
from utils.errors import *
from utils.other import *


def sort_by_datetime(smth):  # функция для сортировки событий по дате и времени
    return smth[2], smth[3], smth[1][0]


# класс главного окна
class MyMainWindow(BaseWindow, design.Ui_mainWindow):

<<<<<<< HEAD
    def __init__(self):
        super().__init__(self)
=======
    def __init__(self, filename):
        super().__init__()
>>>>>>> branch 'main' of https://github.com/Chimnay/imranhello.git
        self.setupUi(self)

        self.addEvent.clicked.connect(self.add_event)
        self.deleteEvent.clicked.connect(self.delete_event)
        self.settingsButton.clicked.connect(self.open_settings)
        self.faqbutton.clicked.connect(self.open_faq)

        self.filename = filename

        self.faqbutton.setStyleSheet("""
            QPushButton {
                image: url(iconsdir/faq.png);
                background-repeat: no-repeat;
                width: 50px;
                height: 50px;
            }
            
            QPushButton:hover {
                image: url(iconsdir/faq1.png);
                background-repeat: no-repeat;
                width: 50px;
                height: 50px;
            }
        """.replace("iconsdir", iconsdir))

        self.settingsButton.setStyleSheet("""
                    QPushButton {
                        image: url(iconsdir/settings.png);
                        background-repeat: no-repeat;
                        width: 50px;
                        height: 50px;
                    }

                    QPushButton:hover {
                        image: url(iconsdir/settings1.png);
                        background-repeat: no-repeat;
                        width: 50px;
                        height: 50px;
                    }
                """.replace("iconsdir", iconsdir))
        self.settingsButton.setText('')

        self.deleteEvent.setStyleSheet("""
                            QPushButton {
                                image: url(iconsdir/delete.png);
                                background-repeat: no-repeat;
                                width: 50px;
                                height: 50px;
                            }

                            QPushButton:hover {
                                image: url(iconsdir/delete1.png);
                                background-repeat: no-repeat;
                                width: 50px;
                                height: 50px;
                            }
                        """.replace("iconsdir", iconsdir))

        self.addEvent.setStyleSheet("""
                                    QPushButton {
                                        image: url(iconsdir/add.png);
                                        background-repeat: no-repeat;
                                        width: 50px;
                                        height: 50px;
                                    }

                                    QPushButton:hover {
                                        image: url(iconsdir/add1.png);
                                        background-repeat: no-repeat;
                                        width: 50px;
                                        height: 50px;
                                    }
                                """.replace("iconsdir", iconsdir))

        with db:  # загрузка данных из бд при запуске программы
            cursor = db.cursor()

            # создание с таблицами с ивентами, если таковой не существует
            cursor.execute('''
                CREATE table IF not exists 
                    events (
                        number integer PRIMARY KEY, 
                        name text, 
                        date text, 
                        time text
                    )
            ''')

            # создание с таблицами с настройками, если таковой не существует
            cursor.execute('''
                CREATE table IF not exists 
                    settings (
                        id integer PRIMARY KEY DEFAULT(1), 
                        autoload integer DEFAULT(0), 
                        language text DEFAULT "eng"
                    )
            ''')

            # вставка стандартных данных в таблицу с настройками, если та не заполнена
            try:
                cursor.execute('''
                    INSERT INTO settings 
                        VALUES (
                            1, 
                            0, 
                            "eng"
                        )
                ''')
            except sqlite3.IntegrityError:
                pass

            # получение языка программы из бд и ее перевод
            self.language = cursor.execute('SELECT language FROM settings').fetchone()[0]
            self.translate(self.language)

            # получение данных о будильниках и добавление их в TableWidget
            data = cursor.execute('SELECT name, date, time FROM events').fetchall()
            self.tableWidget.setRowCount(len(data))
            for i, frag in enumerate(data):
                for j, elem in enumerate(frag):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

        self.update_db()

        # создание потока
        self.thread = QtCore.QThread()
        # создание объекта для выполнения кода в другом потоке
        self.browserHandler = BrowserHandler()
        # перенос объекта в другой поток
        self.browserHandler.moveToThread(self.thread)
        # подключение всех сигналов и слотов
        self.browserHandler.alarmsignal.connect(self.checktime)
        # подключение сигнала старта потока к методу run у объекта,
        # который должен выполнять код в другом потоке
        self.thread.started.connect(self.browserHandler.run)
        self.thread.start()

        self.tableWidget.doubleClicked.connect(self.save_cell)
        self.tableWidget.cellChanged.connect(self.check_change)

    def save_cell(self):
        global previous_cell
        previous_cell = str(self.tableWidget.currentItem().text())

    def check_change(self):
        cell = self.tableWidget.currentItem()
        if cell:
            col = cell.column()

            # time
            if col == 2:
                try:
                    # получение указанной даты
                    event_date_list = self.tableWidget.item(cell.row(), 1).text().split('.')
                    event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                                         int(event_date_list[0]))
                    # проверка, является ли написанная дата прошедшей
                    if event_date < dt.date.today():
                        if self.language == 'rus':
                            raise DateError('Указанная дата меньше текущего')
                        raise DateError('Written date is less than current')
                    # получение текущего и указанного времени
                    current_time = dt.datetime.now().time()
                    event_time = str(cell.text()).split(':')
                    # проверка, введено ли корректно написанное время
                    try:
                        alarm_time = dt.time(hour=int(event_time[0]), minute=int(event_time[1]))
                    except ValueError:
                        if self.language == 'rus':
                            raise TimeError('Время введено не правильно\nФормат времени : ЧЧ:ММ')
                        raise TimeError('Wrong time\nTime\'s format : HH:MM')
                    # проверка, прошло ли написанное время
                    if (alarm_time.hour, alarm_time.minute) < \
                            (current_time.hour, current_time.minute) and \
                            event_date == dt.date.today():
                        if self.language == 'rus':
                            raise TimeError('Указанное время меньше текущего')
                        raise TimeError('Written time is less than current')
                    with db:
                        cursor = db.cursor()
                        cursor.execute(
                            f'UPDATE events SET time = "{cell.text()}" WHERE number = {cell.row() + 1}')

                # обработчик ошибок
                except Exception as ex:
                    if self.language == 'rus':
                        QtWidgets.QMessageBox.warning(self, 'Ошибка при изменении', str(ex),
                                                      QtWidgets.QMessageBox.Ok)
                    else:
                        QtWidgets.QMessageBox.warning(self, 'Error with editing', str(ex),
                                                      QtWidgets.QMessageBox.Ok)
                    self.tableWidget.currentItem().setText(previous_cell)
                    self.tableWidget.currentItem().setTextAlignment(QtCore.Qt.AlignCenter)
                    return

            # date
            elif col == 1:
                try:
                    # получение указанной даты
                    event_date_list = self.tableWidget.item(cell.row(), 1).text().split('.')

                    # проверка, корректно ли написана дата
                    try:
                        event_date = dt.date(int(event_date_list[2]), int(event_date_list[1]),
                                             int(event_date_list[0]))
                    except IndexError:
                        if self.language == 'rus':
                            raise DateError('Дата введена не правильно\nФормат времени: ДД:ММ:ГГГГ')
                        raise DateError('Wrong date\nDate\'s format : DD:MM:YYYY')

                    # проверка, является ли дата прошедшей
                    if event_date < dt.date.today():
                        if self.language == 'rus':
                            raise DateError('Указанная дата меньше текущей')
                        raise DateError('Written date is less than current')

                    with db:
                        cursor = db.cursor()
                        cursor.execute(
                            f'UPDATE events SET date = "{cell.text()}" WHERE number = {cell.row() + 1}')

                    # обработчик ошибок
                except Exception as ex:
                    if self.language == 'rus':
                        QtWidgets.QMessageBox.warning(self, 'Ошибка при изменении', str(ex),
                                                      QtWidgets.QMessageBox.Ok)
                    else:
                        QtWidgets.QMessageBox.warning(self, 'Error with editing', str(ex),
                                                      QtWidgets.QMessageBox.Ok)
                    self.tableWidget.currentItem().setText(previous_cell)
                    self.tableWidget.currentItem().setTextAlignment(QtCore.Qt.AlignCenter)
                    return

            # name
            elif col == 0:
                with db:
                    cursor = db.cursor()
                    cursor.execute(
                        f'UPDATE events SET name = "{cell.text()}" WHERE number = {cell.row() + 1}')

    # получение сигнала с другого потока
    @QtCore.pyqtSlot(str, str)
    def checktime(self, name, time):
        self.alarm(name, time)

    # срабатывание будильника
    def alarm(self, name, times):
        self.wind = AlarmWindow(self, name, times)
        self.wind.show()
        self.update_db()

    # перевод главного окна
    def translate(self, lang):
        if lang == 'eng':
            self.tableWidget.setHorizontalHeaderLabels(['Event', 'Data', 'Time'])
            self.tableWidget.setToolTip('Here you can see your events')

            self.addEvent.setToolTip('This button adds new event')

            self.deleteEvent.setToolTip('This button deletes selected events')

            self.settingsButton.setToolTip('This button opens settings menu')
        elif lang == 'rus':
            self.tableWidget.setHorizontalHeaderLabels(['Событие', "Дата", "Время"])
            self.tableWidget.setToolTip('Тут вы можете увидеть ваши события')

            self.addEvent.setToolTip('Эта кнопка добавляет новое событие')

            self.deleteEvent.setToolTip('Эта кнопка удаляет событие')

            self.settingsButton.setToolTip('Эта кнопка открывает меню настроек')

    # открытие окна с добавлением нового события
    def add_event(self):
        self.addevent = AddEventWindow(self)
        self.addevent.move(self.x(), self.y())
        self.addevent.resize(self.width(), self.height())
        self.addevent.show()

    # открытие окна FAQ
    def open_faq(self):
        self.faq = FAQWindow(self)
        self.faq.move(self.x(), self.y())
        self.faq.resize(self.width(), self.height())
        self.faq.show()

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
        if event.key() == Qt.Key_Delete:  # Удаление элементов из таблицы с помощью кнопки DEL
            self.delete_event()

    def open_settings(self):
        self.settings = SettingsWindow(self)
        self.settings.move(self.x(), self.y())
        self.settings.resize(self.width(), self.height())
        self.settings.show()

    def update_db(self):
        # создаем список из ивентов, чтобы его нормально отсортировать, заливаем его в tablewidget
        events = []
        for i in range(self.tableWidget.rowCount()):
            items = [str(i + 1)]
            for j in range(self.tableWidget.columnCount()):
                items.append(str(self.tableWidget.item(i, j).text()))

            this_date = items[2].split('.')
            this_time = str(items[3]).split(':')
            current_time = dt.datetime.now().time()

            # проверка, прошло ли событие
            if (dt.date(int(this_date[2]), int(this_date[1]), int(this_date[0])) >= dt.date.today()
                    and ((int(this_time[0]), int(this_time[1])) >= (
                            current_time.hour, current_time.minute))):
                events.append(items)

        # сортировка списка с событиями по дате
        events.sort(key=sort_by_datetime)
        for i, event in enumerate(events):
            event[0] = str(i + 1)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(len(events))

        # заливаем отсортированный список в бд
        with db:
            cursor = db.cursor()
            cursor.execute('DELETE FROM events')
            for i, column in enumerate(events):
                cursor.execute('''
                    INSERT INTO events (
                        number, 
                        name, 
                        date, 
                        time
                    ) 
                    VALUES (
                        ?, 
                        ?, 
                        ?, 
                        ?
                    )
                ''', tuple(column))
                for j, elem in enumerate(column[1::]):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

    # close event и закрытие thread на срабатывание таймера
    def closeEvent(self, arg0: QtGui.QCloseEvent) -> None:
        self.stop_thread = True
