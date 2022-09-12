import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


import googletrans


class TranslatorApi():
    def __init__(self):
        self.languages = googletrans.LANGUAGES
        self.language_list = list(self.languages.values())
        self.transator = googletrans.Translator()

    def translate(self, language1, language2, text):
        # Get Original Language Key
        for key, value in self.languages.items():
            if value == language1:
                from_language_key = key

        # Get translated Language Key
        for key, value in self.languages.items():
            if value == language2:
                to_language_key = key

        # translate words
        words = self.transator.translate(text, to_language_key, from_language_key)

        print(words)

        return words.text

    def auto_translate(self, dest_lang, text):
        # Get translated Language Key
        for key, value in self.languages.items():
            if value == dest_lang:
                to_language_key = key

        # translate words

        words = self.transator.translate(text, dest=to_language_key)

        print(words)
        
        return words.text, self.languages[words.src]



html = """
<ui>
  <menubar name='MenuBar'>
    <menu action='HelpMenu'>
      <menuitem action='ShowHelpA'>
      </menuitem>
    </menu>
  </menubar>
</ui>
"""

languages_mock = ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'azerbaijani', 'basque', 'belarusian', 'bengali', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dutch', 'english', 'esperanto', 'estonian', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'korean', 'kurdish (kurmanji)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lithuanian', 'luxembourgish', 'macedonian', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'mongolian', 'myanmar (burmese)', 'nepali', 'norwegian', 'odia', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'romanian', 'russian', 'samoan', 'scots gaelic', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'telugu', 'thai', 'turkish', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']

class Dialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Tłumacz - pomoc", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label='Rozwiń listę języków w celu wybrania języka oryginalnego i docelowego.\nWprowadz tekst do przetłumaczenia do lewego pola na tekst.\nWciśnij przycisk "Tłumacz", w celu przetłumaczenia tekstu. Przetłumaczony tekst wyświetli się w prawym polu tekstowym.\nWciśnij przycisk "Zamień języki", aby zamienić miejscami języki.\nZaznacz pole automatyczne wykrywanie języka, w celu automatycznego wykrycia języka oryginalnego tekstu w lewym polu tekstowym.')
        box = self.get_content_area()
        box.add(label)
        self.show_all()


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Tłumacz")
        self.Translator = TranslatorApi()

        self.set_default_size(620, 570)

        action_group = Gtk.ActionGroup(name="my_actions")

        self.add_file_menu_actions(action_group)

        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)

        menubar = uimanager.get_widget("/MenuBar")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(menubar, False, False, 0)
        self.add(box)

        combos = self.add_combo_boxes()
        box.pack_start(combos, False, False, 0)

        buttons = self.add_buttons()
        box.pack_start(buttons, False, False, 40)

        self.checkbox = Gtk.CheckButton("Automatyczne tłumaczenie tekstu")
        hbox = Gtk.Box()
        hbox.pack_start(self.checkbox, False, False, 70)
        box.pack_start(hbox, False, False, 10)

    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action(name="HelpMenu", label="Pomoc")
        action_group.add_action(action_filemenu)

        action_new = Gtk.Action(
            name="ShowHelpA",
            label="_Pokaż pomoc",
            tooltip="",
            stock_id=Gtk.STOCK_NEW,
        )
        action_new.connect("activate", self.on_menu_file_new_generic)
        action_group.add_action(action_new)

    def create_ui_manager(self):
        uimanager = Gtk.UIManager()

        # Throws exception if something went wrong
        uimanager.add_ui_from_string(html)

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    def on_menu_file_new_generic(self, a):
        dialog = Dialog(self)
        dialog.run()
        dialog.destroy()

    def add_combo_boxes(self):
        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        languages = self.Translator.language_list
        # languages = languages_mock

        self.languages_combo1 = Gtk.ComboBoxText()

        self.languages_combo2 = Gtk.ComboBoxText()

        for language in languages:
            self.languages_combo1.append(language, language)
            self.languages_combo2.append(language, language)

        self.languages_combo1.set_active_id("afrikaans")
        self.languages_combo2.set_active_id("afrikaans")

        left.pack_start(self.languages_combo1, False, False, 10)
        right.pack_start(self.languages_combo2, False, False, 10)

        self.left_input = Gtk.Entry()
        self.left_input.set_text("")

        self.right_input = Gtk.Entry()
        self.right_input.set_text("")

        left.pack_start(self.left_input, False, False, 0)
        right.pack_start(self.right_input, False, False, 0)

        hbox = Gtk.Box()
        hbox.pack_start(left, True, False, 10)
        hbox.pack_end(right, True, False, 10)
        return hbox

    def add_buttons(self):
        hbox = Gtk.Box()

        self.translate_button = Gtk.Button.new_with_label("Tłumacz")
        self.translate_button.connect("clicked", lambda _: self.translate())
        self.switch_button = Gtk.Button.new_with_label("Zamień języki")
        self.switch_button.connect("clicked", lambda _: self.switch())
        hbox.pack_start(self.translate_button, False, False, 70)
        hbox.pack_start(self.switch_button, False, False, 10)

        return hbox

    def translate(self):
        text_to_translate = self.left_input.get_text()
        print('Tłumaczę: ')
        print(text_to_translate)

        lang1 = self.languages_combo1.get_active_text()
        lang2 = self.languages_combo2.get_active_text()
        print(lang1, lang2)

        if not self.checkbox.get_active():
            text_translated = self.Translator.translate(lang1, lang2, text_to_translate)
            # text_translated = "hej"
        else:
            text_translated, src_language = self.Translator.auto_translate(lang2, text_to_translate)
            # text_translated, src_language = "hej", "polish"
            print("src=")
            print(src_language)
            self.languages_combo1.set_active_id(src_language)
            
        print('Przetłumaczono : ' + text_translated)
        self.right_input.set_text(text_translated)

    def switch(self):
        lang1 = self.languages_combo1.get_active_text()
        lang2 = self.languages_combo2.get_active_text()
        self.languages_combo2.set_active_id(lang1)
        self.languages_combo1.set_active_id(lang2)
        self.left_input.set_text(self.right_input.get_text())
        self.right_input.set_text("")
        self.translate()

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()