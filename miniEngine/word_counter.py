import Trie
import os
import unittest
import pretreater

class word_cunter:
    def __init__(self):
        # 一个dict，用来存放文件夹Shakespeare下的所有txt文件的文件名，并生成对应的id
        self.all_works = {}
        # 一个int，用来记录Shakespeare文件夹下的文件总个数
        self.num_document = 0
        # 一个string，用来存放Shakespeare文件夹的相对路径
        self.path = ''
        # 一个trie，用来存放inverted index
        self.new_trie = Trie.Trie()
        # 一个list，用来存放所有的stop words
        self.stop_words = []
        # 一个pretreater, 包含了split，filter，stemmer等组件
        self.pre = pretreater.pretreater()

    def set_path(self, p: str): # 为project1， 这里默认path是文件夹Shakespeare的path
        self.path = p

    def get_all_works(self):
        id = 0
        for i in os.listdir(self.path):
            if i != '.DS_Store':      # 忽略.DS文件
                self.all_works[i] = id
                id += 1
                self.num_document += 1

    def word_counter(self):
        for work_name in self.all_works:
            file_name = self.path + work_name
            curr_words = self.pre.final_stemmer(file_name)
            curr_dict = {}
            for word in curr_words:
                if word not in curr_dict:
                    curr_dict[word] = 1
                else:
                    curr_dict[word] += 1
            # print(curr_dict)
            for word in curr_dict:
                self.new_trie.insert(word, work_name, curr_dict[word])

class word_counter_test(unittest.TestCase):
    def test_get_all_works(self):
        wc = word_cunter()
        wc.set_path("text/Shakespeare/")
        wc.get_all_works()
        print(wc.all_works)
        # 测试通过
        self.assertEqual(wc.num_document, len(wc.all_works))
        self.assertEqual(wc.num_document, 42) # 总共有42部作品

    def test_word_count_file_name(self):
        wc = word_cunter()
        wc.set_path('text/Shakespeare/')
        wc.get_all_works()
        for work_name in wc.all_works:
            file_name = wc.path + work_name
            print(file_name)

        # 输出形式：text/Shakespeare/TitusAndronicus.txt
        # 测试通过

    def test_word_count_small(self):
        wc = word_cunter()
        wc.set_path('text/small_test/')
        wc.get_all_works()
        wc.word_counter()
        curr_tire = wc.new_trie
        self.assertEqual(curr_tire.is_exist('play').content.get('sentence_test.txt'), 2)
        self.assertEqual(curr_tire.is_exist('play').content.get('word_count_small_test.txt'), 2)



    def test_word_count_large(self):
        wc = word_cunter()
        wc.set_path('text/Shakespeare_small_test/')
        wc.get_all_works()
        wc.word_counter()