from PyQt5 import QtGui

from uis import settings
from connects import db

from Windows.Window import BaseWindow


# класс для окна настроек
class SettingsWindow(settings.Ui_MainWindow, BaseWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        # [x.clicked.connect(self.sql_autoload) for x in self.autoload_group.buttons()]
        [x.clicked.connect(self.sql_language) for x in self.language_group.buttons()]

        # загрузка данных из бд при открытии окна настроек
        with db:
            cursor = db.cursor()
            autoload = cursor.execute('''
                                        SELECT 
                                            autoload 
                                        FROM 
                                            settings''').fetchone()[0]
            lang = cursor.execute('''SELECT 
                                        language 
                                    FROM 
                                        settings''').fetchone()[0]
            self.translate(lang)

        # изменение radiobuttons в зависимости от значений из бд
        if autoload:
            self.radioButton_3.setChecked(True)
            self.radioButton_4.setChecked(False)
        else:
            self.radioButton_3.setChecked(False)
            self.radioButton_4.setChecked(True)
        if lang == 'eng':
            self.radioButton.setChecked(True)
            self.radioButton_2.setChecked(False)
        elif lang == 'rus':
            self.radioButton_2.setChecked(True)
            self.radioButton.setChecked(False)

    # def sql_autoload(self):
    # вырезанный функционал(
    # with db:
    # cursor = db.cursor()
    # if self.sender().text() == 'Ya':
    # cursor.execute('''UPDATE
    #                       settings
    #                   SET
    #                       autoload = 1''')

    # elif self.sender().text() == 'No':
    # cursor.execute('''
    #                   UPDATE
    #                       settings
    #                   SET
    #                       autoload = 0''')

    # обновление языка программы в базе данных
    def sql_language(self):
        with db:
            lng = self.sender().text()
            cursor = db.cursor()
            cursor.execute(f'''
                            UPDATE 
                                settings 
                            SET 
                                language = "{lng}"''')
            self.parent.language = lng

        self.translate(lng)

    # функция перевода окна
    def translate(self, lang):
        if lang == 'eng':
            self.radioButton_3.setToolTip('This feature will be available in close future.')
            self.radioButton_4.setToolTip('This feature will be available in close future.')
            self.label_2.setToolTip('This feature will be available in close future.')
            self.radioButton.setToolTip(
                'Tick this if you want to see this program on English language')
            self.radioButton_2.setToolTip(
                'Tick this if you want to see this program on Russian language')

            self.label_2.setText('Autoload')
            self.label.setText('Language')

            self.setWindowTitle('Settings')

        elif lang == 'rus':
            self.radioButton_3.setToolTip('Эта функция будет доступна в ближайшем будущем.')
            self.radioButton_4.setToolTip('Эта функция будет доступна в ближайшем будущем.')
            self.label_2.setToolTip('Эта функция будет доступна в ближайшем будущем.')

            self.radioButton.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на пендосском языке')
            self.radioButton_2.setToolTip(
                'Отметьте это, если вы хотите, чтобы эта программа была на великом и могучем языке')

            self.label_2.setText('Автозагрузка')
            self.label.setText('Язык')

            self.setWindowTitle('Настройки')

    # обнеовление языка основного окна при закрытии этого
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        with db:
            cursor = db.cursor()
            lang = cursor.execute('''
                                    SELECT 
                                        language 
                                    FROM 
                                        settings''').fetchone()[0]
        self.parent.translate(lang)
