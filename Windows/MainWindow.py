import sqlite3

from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidgetItem

from Windows.AlarmWindow import AlarmWindow
from Windows.FAQWindow import FAQWindow
from uis import design
from UsefulShit import db, BrowserHandler

from Windows.AddEventWindow import AddEventWindow
from Windows.SettingsWindow import SettingsWindow
from Windows.Window import BaseWindow


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
        self.faqbutton.clicked.connect(self.open_faq)

        self.faqbutton.setStyleSheet("""
                                        QPushButton{
                                            image: url(files//faq.png);
                                            background-repeat: no-repeat;
                                            width: 50px;
                                            height: 50px;
                                                    }
                                        QPushButton:hover {
                                            image: url(files//faq1.png);
                                            background-repeat: no-repeat;
                                            width: 50px;height: 50px;
                                                            }""")

        # загрузка данных из бд при запуске программы
        with db:
            cursor = db.cursor()

            # создание с таблицами с ивентами, если таковой не существует
            cursor.execute('''
                            CREATE 
                                table 
                            IF 
                                not exists 
                            events (
                                number integer PRIMARY KEY, 
                                name text, 
                                date date, 
                                time time
                                                                  )
                            ''')
            # создание с таблицами с настройками, если таковой не существует
            cursor.execute('''
                            CREATE 
                                table 
                            IF 
                                not exists 
                            settings (
                                id integer PRIMARY KEY DEFAULT(1), 
                                autoload integer DEFAULT(0), 
                                language text DEFAULT "eng"
                                                                    )
                            ''')
            # вставка дефолтных данных в таблицу с настройками, если та не заполнена
            try:
                cursor.execute('''
                                INSERT INTO 
                                    settings 
                                VALUES (
                                        1, 
                                        0, 
                                        "eng"
                                                )
                                ''')
            except sqlite3.IntegrityError:
                pass

            # получение языка программы из бд и ее перевод
            self.language = cursor.execute('''
                                            SELECT 
                                                language 
                                            FROM 
                                                settings
                                            ''').fetchone()[0]
            self.translate(self.language)

            # получение данных о будильниках и добавление их в TableWidget
            data = cursor.execute('''
                                    SELECT 
                                        name, date, time 
                                    FROM 
                                        events''').fetchall()
            self.tableWidget.setRowCount(len(data))
            for i, frag in enumerate(data):
                for j, elem in enumerate(frag):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))

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
        # запуск потока
        self.thread.start()

    # получение сигнала с другого потока
    @QtCore.pyqtSlot(str, str)
    def checktime(self, name, time):
        self.alarm(name, time)

    # срабатывание будильника
    def alarm(self, name, times):
        self.wind = AlarmWindow(name, times)
        self.wind.show()

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

    # открытие окна FAQ
    def open_faq(self):
        self.faq = FAQWindow()
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
            cursor.execute('''
                            DELETE 
                            FROM 
                                events''')
            for i, column in enumerate(events):
                cursor.execute('''
                                INSERT INTO 
                                    events (
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
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.stop_thread = True
