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


tr = TranslatorApi()
print(tr.language_list)

