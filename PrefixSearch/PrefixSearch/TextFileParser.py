from re import findall

class TextFileParser:
    def __init__(self, text_file_info):
        self._file_info = text_file_info

    def get_words_from_file(self):
        file = open(self._file_info.get_full_name(), 'r')
        file_data = file.read()
        file.close()
        return [str.lower(word) for word in findall(r"[A-Za-z']+", file_data)]



