import Trie
import os
import unittest

class word_cunter:
    def __init__(self):
        # 一个dict，用来存放文件夹Shakespeare下的所有txt文件的文件名，并生成对应的id
        self.all_works = {}
        # 一个int，用来记录Shakespeare文件夹下的文件总个数
        self.num_document = 0
        # 一个string，用来存放Shakespeare文件夹的相对路径
        self.path = ""
        # 一个trie，用来存放inverted index
        self.new_trie = Trie.Trie()
        # 一个list，用来存放所有的stop words
        self.stop_words = []
        # 一个stemmer, 到时候再定义

    def set_path(self, p: str): # 为project1， 这里默认path是文件夹Shakespeare的path
        self.path = p

    # 设置word counter中的stop words表，可以通过更改这个函数改变stop words表
    # 理论上来说，任何在stop words中出现过的单词，在最后的trie中都不能找到！！
    def set_stopwords(self):
        # stop words 来自于nltk.corpus
        # 资源来自于 https://www.nltk.org/data.html
        self.stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
                           'you', "you're", "you've", "you'll", "you'd", 'your', 'yours',
                           'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
                           "she's", 'her', 'hers', 'herself', 'it', "it's", 'its',
                           'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                           'what', 'which', 'who', 'whom', 'this', 'that', "that'll",
                           'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
                           'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
                           'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                           'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
                           'into', 'through', 'during', 'before', 'after', 'above', 'below',
                           'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under',
                           'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where',
                           'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other',
                           'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                           'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
                           "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're',
                           've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
                           'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't",
                           'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
                           "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't",
                           'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 's']

    # 这个函数的输入是一个word的list，输出是word的list，中间进行了去除stop word的操作
    def delete_stop_words(self, words: list):
        for word in words:
            if word in self.stop_words:
                words.remove(word)

        return words

    def get_all_works(self):
        id = 0
        for i in os.listdir(self.path):
            self.all_works[i] = id
            id += 1
            self.num_document += 1




class word_counter_test(unittest.TestCase):
    def test_get_all_works(self):
        wc = word_cunter()
        wc.set_path("text/Shakespeare/")
        wc.get_all_works()
        print(wc.all_works)
        # 期望output：{'test1.txt': 0, 'test2.txt': 1}
        # 实际output：{'test1.txt': 0, 'test2.txt': 1}
        # 测试通过
        self.assertEqual(wc.num_document, 2)