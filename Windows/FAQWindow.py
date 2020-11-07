from Windows.Window import BaseWindow
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

    def translate(self, lang):
        if lang == 'rus':
            self.pushButton.setText(
                f'Мелодии напоминания в папке {musicdir}. Только .wav файлы, возможна конвертация в настройках')
            self.pushButton_3.setText('Не удаляйте содержимое и сами папки icons, textures.')
            self.pushButton_4.setText(
                "Внутри программы события не изменять, только удалять и доабвлять новые через кнопки")
            self.pushButton_2.setText('Присутствует ненормативная лексика')
        elif lang == 'eng':
            self.pushButton.setText(
                f'Alarm music in folder {musicdir}. Only .wav files, convertation avaliable in settings')
            self.pushButton_3.setText("Dont chavge event in program, only add and delete with buttons")
            self.pushButton_4.setText('Do not delete icons, textures folders and its content.')
            self.pushButton_2.setText('profanity is present')
        self.pushButton_6.setText('Credits:\nSvyatoslav Svyatkin\nImran Amirov')
