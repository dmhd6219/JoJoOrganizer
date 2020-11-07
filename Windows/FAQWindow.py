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
            self.pushButton.setText(
                'Музыку добавлять в папку /files/music. Используются wav файлы, возможна конвертация в настройках')
            self.pushButton_2.setText(
                "Внутри программы события не менять, только удалять и доабвлять новые через кнопки")
            self.pushButton_3.setText('Присутствует ненормативная лексика')
            self.pushButton_4.setText(
                'Фотографии из папки files, саму папку files и папку music не удалять.')
            self.pushButton_5.setText('Вроде бы все')
        elif lang == 'eng':
            self.pushButton.setText(
                'Add music to folder /files/music. Using wav files, convertation avaliable in settings')
            self.pushButton_2.setText(
                "Dont chavge event in program, only add and delete with buttons")
            self.pushButton_3.setText('profanity is present')
            self.pushButton_4.setText(
                'Do not delete photos from the files folder,'
                ' the files folder itself and the music folder.')
            self.pushButton_5.setText('I suppose, thats all')
        self.pushButton_6.setText(
            'Credits:\nSvyatoslav Svyatkin\nImran Amirov')
