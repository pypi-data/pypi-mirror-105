import os
import re

class DirectoryTree():

    pattern = r"\.error$"
    
    def __init__(self, base_dir, pattern):
        self.base_dir = base_dir
        self.pattern = pattern
        self.list_file = []
        self.dict_file = {}
        self.main()

    def join_path(self, base, folder):
        return os.path.join(base, folder)
        
    def match_file(self, file_name):
        """
        :return: True if word mach.
        :rtype: bool
        """
        result = re.findall(self.pattern, file_name)
        return result

    def main(self):
        self.list_file, self.dict_file = self.recusive_folder(self.base_dir)

    def recusive_show(self, list_folder, prefix="│"):
        last_key = list(list_folder)[-1]
        for item in list_folder:
            item_tmp = list_folder[item]
            if type(item_tmp) == str:
                if last_key == item:
                    print(prefix[:-1] + "└─ " + item)
                else:
                    print(prefix + "─ " + item)

            elif type(item_tmp) == dict:
                if len(item_tmp) <= 0:
                    continue
                if last_key == item:
                    print(prefix[:-1] + "└─ " + item + "/")
                    self.recusive_show(item_tmp, prefix[:-1] + "   │")
                else:
                    print(prefix + "─ " + item + "/")
                    self.recusive_show(item_tmp, prefix + "  │")

    def show(self, is_tree=True):
        print(self.base_dir)
        if len(self.list_file) == 0:
            print("No file")
        else:
            if is_tree:
                self.recusive_show(self.dict_file)
            else:
                for i in self.list_file:
                    print(i)
        
    def recusive_folder(self, path):
        list_dir = os.listdir( path )
        list_file_tmp = []
        dict_file_tmp = {}
        for item in list_dir:
            dict_file_tmp[item] = {}
            attachmet_path = self.join_path(path, item)
            
            if os.path.isdir(attachmet_path):
                list_dirs_re, dict_file_re = self.recusive_folder(attachmet_path)
                
                dict_file_tmp[item] = dict_file_re
                if len(dict_file_re) <= 0:
                    del dict_file_tmp[item]
                list_file_tmp = list_file_tmp + list_dirs_re

            elif os.path.isfile(attachmet_path) and self.pattern and self.match_file(item):
                dict_file_tmp[item] = 'file'
                list_file_tmp.append(attachmet_path)

            else:
                del dict_file_tmp[item]

        return list_file_tmp, dict_file_tmp