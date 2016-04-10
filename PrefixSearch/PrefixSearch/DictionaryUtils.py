from TextFileParser import TextFileParser
from EntryInfo import EntryInfo
from collections import defaultdict

class DictionaryUtils:
    def __init__(self):
        self._word_count_dict = {}
        self._count_words_dict = {}
        self._words_trie = {}

    ############################################

    def parse_from_dir_list(self, dir_list):
        fileinfo_list = self.get_text_fileinfo_list(dir_list)
        self._word_count_dict = self.parse_text_files(fileinfo_list)
        
        self.create_count_words_dict()
        self.create_words_trie()

    def get_text_fileinfo_list(self, dir_list):
        fileinfo_list = []
        for dirinfo in [EntryInfo(dir_path) for dir_path in dir_list]:
            if dirinfo.is_dir():
                fileinfo_list += dirinfo.get_text_fileinfo_list_recursively()
        return fileinfo_list

    def parse_text_files(self, fileinfo_list):
        word_count_dict = {}
        for file_info in fileinfo_list:
            for word in TextFileParser(file_info).get_words_from_file():
                word_count_dict[word] = word_count_dict.setdefault(word, 0) + 1
        return word_count_dict

    ############################################

    def parse_from_dict_file(self, file_name):
        file_data = self.get_file_data(file_name)
        self._count_words_dict = self.parse_dict_file_data(file_data)

        self.create_word_count_dict()
        self.create_words_trie()

    def get_file_data(self, file_name):
        file = open(file_name, 'r')
        file_data = file.read()
        file.close()
        return file_data

    def parse_dict_file_data(self, file_data):
        count_words_dict = {}
        file_lines = file_data.split(sep = "\n")
        if len(file_lines) > 1:
            for line in file_lines[1:]:
                items = line.split()
                if len(items) > 1:
                    count = int(items[0])
                    words_list = items[1:]
                    count_words_dict[count] = words_list
        return count_words_dict

    ############################################

    def create_count_words_dict(self):
        for word,count in self._word_count_dict.items():
            self._count_words_dict.setdefault(count, set([])).add(word)

    def create_word_count_dict(self):
        for count,words in self._count_words_dict.items():
            for word in words:
                self._word_count_dict[word] = count

    def create_words_trie(self):
        for word in self._word_count_dict.keys():
            cur_dict = self._words_trie
            for c in word:
                cur_dict = cur_dict.setdefault(c, {})
            cur_dict[None] = None

    ############################################

    def get_word_count_dict(self):
        return self._word_count_dict

    def get_count_words_dict(self):
        return self._count_words_dict

    def get_words_trie(self):
        return self._words_trie

    #############################################

    def save_dict_to_file(self, file_name):
        file = open(file_name, 'w')
        file.write(str(len(self._word_count_dict)) + "\n")
        for count in sorted(self._count_words_dict.keys(), reverse=True):
            file.write(' '.join([str(count)] + list(self._count_words_dict[count])) + "\n")
        file.close()

    #############################################
 
    def get_words_from_trie(self, prefix, trie_dict):
        result = []
        for c in trie_dict.keys():
            if c != None:
                result += self.get_words_from_trie(prefix + c, trie_dict[c])
            else:
                result += [prefix]
        return result

    def find_all_by_prefix(self, prefix):
        cur_dict = self._words_trie
        for c in str.lower(prefix):
            if c not in cur_dict.keys():
                return []
            cur_dict = cur_dict[c]
        return sorted(self.get_words_from_trie(prefix, cur_dict), 
                      key = lambda word : self._word_count_dict[word], 
                      reverse = True)

