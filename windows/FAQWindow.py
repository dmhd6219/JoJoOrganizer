from windows.Window import BaseWindow
from uis import faq
from utils.other import *


class FAQWindow(BaseWindow, faq.Ui_MainWindow):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)
        self.setupUi(self)
        self.setWindowTitle('FAQ')

        with db:
            cursor = db.cursor()
            self.translate(self.mainWindow.language)

    # функция перевода
    def translate(self, lang):
        if lang == 'rus':
            self.pushButton.setText(
                f'Мелодии напоминания в папке /files/music. \nТолько .wav и .mp3 файлы, возможна конвертация в настройках')
            self.pushButton_4.setText('Не удаляйте папки и их содержимое')
            self.pushButton_2.setText('Присутствует ненормативная лексика')
        elif lang == 'eng':
            self.pushButton.setText(
                f'Alarm music in folder /files/music. \nOnly .wav and .mp3 files, convertation avaliable in settings')
            self.pushButton_4.setText('Do not delete icons, textures folders and its content.')
            self.pushButton_2.setText('profanity is present')
        self.pushButton_6.setText('Credits:\nSvyatoslav Svyatkin\nImran Amirov')
