from mimetypes import guess_type
from os import listdir
from os.path import isfile, join

class EntryInfo:
    """
    Class to store file or folder information,
    like file name, full file name, type of file, etc.
    """
    def __init__(self, dir_path, file_name = ""):
        self._dir_path = dir_path
        self._file_name = file_name
        self._full_name = join(dir_path, file_name)

        self._is_file = isfile(self._full_name)
        self._is_dir = not self._is_file
        self._file_type = guess_type(self._full_name)

        if self._is_dir:
            self._entryinfo_list = [EntryInfo(self._full_name, file_name) for file_name in listdir(self._full_name)]
        else:
            self._entryinfo_list = []

    def get_short_name(self):
        return self._file_name

    def get_full_name(self):
        return self._full_name

    def __str__(self):
        return str(self._full_name)

    def __repr__(self):
        return str(self._full_name)

    def is_file(self):
        return self._is_file

    def is_dir(self):
        return self._is_dir

    def is_text_file(self):
        return self._is_file and self._file_type[0] == 'text/plain'

    def get_entryinfo_list(self):
        return self._entryinfo_list

    def get_dirinfo_list(self):
        return [file_info for file_info in self._entryinfo_list if file_info.is_dir()]

    def get_fileinfo_list(self):
        return [file_info for file_info in self._entryinfo_list if file_info.is_file()]

    def get_text_fileinfo_list(self):
        return [file_info for file_info in self._entryinfo_list if file_info.is_text_file()]

    def get_text_fileinfo_list_recursively(self):
        full_fileinfo_list = self.get_text_fileinfo_list()

        for dirinfo in self.get_dirinfo_list():
            full_fileinfo_list += dirinfo.get_text_fileinfo_list_recursively()
        return full_fileinfo_list



