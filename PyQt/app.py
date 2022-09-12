import sys
sys.path.append("..")
from Translator_api.translator_api import TranslatorApi

from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSlot


class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        
        super(MyWindow, self).__init__(parent)

        self.setWindowTitle("Tłumacz")
        
        layout = QVBoxLayout()
        self.stacklayout = QStackedLayout()

        self.Translator = TranslatorApi()

        #  TODO menu
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.setMovable(False)
        
        

        button_action = QAction("Pomoc", self)
        button_action.setStatusTip("Wyświetla pomoc")
        button_action.triggered.connect(self.showHelp)
        toolbar.addAction(button_action)


        # drop down menu języki
        self.language1 = 'afrikaans'
        self.language2 = 'afrikaans'

        print(self.Translator)

        languages = self.Translator.language_list

        self.combobox_language1 = QComboBox(self)
        self.combobox_language1.addItems(languages)
        self.combobox_language1.move(20, 30)
        self.combobox_language1.resize(280, 40)

        self.combobox_language1.currentTextChanged.connect(self.language1_changed)

        self.combobox_language2 = QComboBox(self)        
        self.combobox_language2.addItems(languages)
        self.combobox_language2.move(320, 30)
        self.combobox_language2.resize(280,40)

        self.combobox_language2.currentTextChanged.connect(self.language2_changed)

        # Pole do wprowadzenia tekstu do przetłumaczenia
        self.textbox_to_translate = QLineEdit(self)
        self.textbox_to_translate.move(20, 70)
        self.textbox_to_translate.resize(280,40)

        # Pole do wyświetlania tekstu przetłumaczonego
        self.textbox_translated = QLineEdit(self)
        self.textbox_translated.move(320, 70)
        self.textbox_translated.resize(280,40)
        
        # Przycisk aktywujący tłumacz
        self.button = QPushButton('Tłumacz', self)
        self.button.move(20,130)

        self.button.clicked.connect(self.translate)

        # Przycisk zamieniający języki
        self.change_language_button = QPushButton('Zamień języki', self)
        self.change_language_button.move(150,130)

        self.change_language_button.clicked.connect(self.change_languages)

        # Checkbox włączający automatyczny język
        self.checkbox_auto_language = QCheckBox("Automatyczne wykrywanie języka", self)
        self.checkbox_auto_language.move(20,155)
        self.checkbox_auto_language.resize(320,40)

        self.checkbox_auto_language.stateChanged.connect(self.auto_language)
        self.auto_language_on = False

        # pomoc dialog
        self.dialogs = list()
        help = self.menuBar().addMenu("&Pomoc")
        ac = help.addAction("Pokaż pomoc")
        ac.triggered.connect(self.showHelp)


    def showHelp(self):
        hw = HelpWindow()
        self.dialogs.append(hw)
        hw.show()

    @pyqtSlot()
    def translate(self):
        # log
        t = 'Jezyk 1: ' + self.language1
        print(t)
        t = 'Jezyk 2: ' + self.language2
        print(t)

        text_to_translate = self.textbox_to_translate.text()
        # log
        print('Tłumaczę: ')
        print(text_to_translate)
        print(type(self.language1))
        print(type(text_to_translate))

        if not self.auto_language_on:
            text_translated = self.Translator.translate(self.language1, self.language2, text_to_translate)
        else:
            text_translated, src_language = self.Translator.auto_translate(self.language2, text_to_translate)
            self.language1 = src_language
            index = self.Translator.language_list.index(src_language)
            self.combobox_language1.setCurrentIndex(index)
        
        # log
        print('Przetłumaczono : ' + text_translated)

        self.textbox_translated.setText(text_translated)
    
    def change_languages(self):
        # log
        print('Zamiana języków')

        temp = self.combobox_language1.currentIndex()
        self.combobox_language1.setCurrentIndex(self.combobox_language2.currentIndex())
        self.combobox_language2.setCurrentIndex(temp)
        self.textbox_to_translate.setText(self.textbox_translated.text())
        self.textbox_translated.setText("")
        # self.translate()
    
    def auto_language(self):
        self.auto_language_on = self.checkbox_auto_language.isChecked()
        if self.checkbox_auto_language.isChecked() == True:
            print('Automatyczne tłumaczenie tekstu')
        else:
            print('Wybierz sam język')
    
    def language1_changed(self, l):
        print("Text changed:", l)
        self.language1 = l

    def language2_changed(self, l):
        print("Text changed:", l)
        self.language2 = l



class HelpWindow(QMainWindow):

    def __init__(self, parent=None):
        super(HelpWindow, self).__init__(parent)
        self.setWindowTitle('Tłumacz - pomoc')
        self.setGeometry(200, 80, 100, 80)
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._generalLayout = QVBoxLayout()
        self._centralWidget.setLayout(self._generalLayout)
        self._generalLayout.addWidget(QLabel('Rozwiń listę języków w celu wybrania języka oryginalnego i docelowego.\nWprowadz tekst do przetłumaczenia do lewego pola na tekst.\nWciśnij przycisk "Tłumacz", w celu przetłumaczenia tekstu. Przetłumaczony tekst wyświetli się w prawym polu tekstowym.\nWciśnij przycisk "Zamień języki", aby zamienić miejscami języki.\nZaznacz pole automatyczne wykrywanie języka, w celu automatycznego wykrycia języka oryginalnego tekstu w lewym polu tekstowym.'))

def start_app():
    app = QApplication(sys.argv)
    app.setApplicationName('Tłumacz')

    main = MyWindow()
    main.setFixedSize(620, 550)
    main.show()

    sys.exit(app.exec())

start_app()
