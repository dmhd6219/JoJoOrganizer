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
                "Музыку добавлять в папку /files/music. Работают только wav файлы\n"
                "Внутри программы события не менять, только удалять и доабвлять новые через кнопки"
                "\nПрисутствует ненорматичная лексика\n"
                "Фотографии из папки files, саму папку files и папку music не удалять."
                "\nВроде бы все\n\n\n\n"
                "Credits:\n             Svyatoslav Svyatkin\n               Imran Amirov")
        elif lang == 'eng':
            self.label.setText('Add music to folder /files/music. Only wav files are working\n'
                               'Dont chavge event in program, only add and delete with buttons\n'
                               '\nUnnormal vocabulary is present\n'
                               'Do not delete photos from the files folder,'
                               ' the files folder itself and the music folder.'
                               'I suppose, thats all\n\n\n\nCredits:\n             Svyatoslav'
                               ' Svyatkin\n             Imran Amirov')
