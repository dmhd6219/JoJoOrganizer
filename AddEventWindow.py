from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

import addevent
from connects import db

from Window import BaseWindow


# класс для окна с добавлением нового события
class AddEventWindow(addevent.Ui_MainWindow, BaseWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.pushButton.clicked.connect(self.additem)
        with db:
            cursor = db.cursor()
            self.lang = cursor.execute('''
                `                       SELECT 
                                            language 
                                        FROM 
                                            settings''').fetchone()[0]
            self.translate = self.translate(self.lang)

    # добавление нового значения в таблицу и обновление базы данных
    def additem(self):
        name = self.lineEdit.text()
        if name:
            self.parent.tableWidget.setRowCount(self.parent.tableWidget.rowCount() + 1)
            self.parent.tableWidget.setItem(self.parent.tableWidget.rowCount() - 1, 0,
                                            QTableWidgetItem(name))
            self.parent.tableWidget.setItem(self.parent.tableWidget.rowCount() - 1, 1,
                                            QTableWidgetItem(self.dateEdit.text()))
            self.parent.tableWidget.setItem(self.parent.tableWidget.rowCount() - 1, 2,
                                            QTableWidgetItem(self.timeEdit.text()))
            self.parent.update_db()
            self.close()
        else:
            if self.lang == 'eng':
                self.message = QMessageBox.warning(self, 'Warning', 'Please input name of ur event',
                                                   QMessageBox.Cancel)
            elif self.lang == 'rus':
                self.message = QMessageBox.warning(self, 'Предупреждение',
                                                   'Пожалуйста, введите название для вашего события',
                                                   QMessageBox.Cancel)

    # перевод окна с добавлением нового события
    def translate(self, lang):
        if lang == 'eng':
            self.label_2.setText('Event name')
            self.label.setText('Date')
            self.label_3.setText('Time')
            self.pushButton.setText('Add event')

            self.lineEdit.setToolTip('Write here ur event\'s name')
            self.timeEdit.setToolTip('Choose date and time of ur event')
            self.pushButton.setToolTip('Press this button to add this event')

            self.setWindowTitle('Add new event')


        elif lang == 'rus':
            self.label_2.setText('Название события')
            self.label.setText('Дата')
            self.label_3.setText('Время')
            self.pushButton.setText('Добавить событие')

            self.lineEdit.setToolTip('Напишите здесь название вашего события')
            self.timeEdit.setToolTip('Выберите дату и время вашего события')
            self.pushButton.setToolTip('Нажмите эту кнопку, чтобы добавить новое событие')

            self.setWindowTitle('Добавить новое событие')
