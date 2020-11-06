from Windows.Window import BaseWindow
from uis import faq
from UsefulShit import db


class FAQWindow(faq.Ui_MainWindow, BaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('FAQ')

        with db:
            cursor = db.cursor()
            self.lang = cursor.execute('''
                                       SELECT 
                                            language 
                                        FROM 
                                            settings
                                                        ''').fetchone()[0]
            self.translate(self.lang)

    def translate(self, lang):
        if lang == 'rus':
            self.label.setText(
                "Музыку добавлять в папку /files/music\n"
                "Внутри программы события не менять, только удалять и доабвлять новые через кнопки"
                "\nВроде бы все")
        elif lang == 'eng':
            self.label.setText('Add music to folder /files/music\n'
                               'Dont chavge event in program, only add and delete with buttons\n'
                               'I suppose, thats all')
