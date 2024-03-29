import unittest

"""
wordcounter的雏形，不进行stemming和filtering的wordcounter
在最终的成品中没有用到
但是在在较为简单的test case中有作为参照出现
"""

class naive_word_counter:
    def __init__(self):
        self.word_count = {}
        self.word_list = []

    # 读取文件的函数
    def open_file(self, file_name: str):
        with open(file_name, 'r') as f:
            for line in f:
                splited = line.split() # 每一行按照空格split
                for word in splited:
                    self.word_list.append(word)

    # 进行word count
    def naive_word_count(self):
        for word in self.word_list:
            if word in self.word_count:
                self.word_count[word] += 1
            else :
                self.word_count[word] = 1
    # 在每次count不同的文件之前都需要reset一下，清空wordlist
    def reset(self):
        self.word_list.clear()
        self.word_count.clear()

class Test(unittest.TestCase):
    def test_1000_words(self):
        file_name = "text/test/random_word_list_1000.txt"
        wc = naive_word_counter()
        wc.open_file(file_name)
        wc.naive_word_count()
        print(wc.word_count)

if __name__ == '__main__':
    unittest.main()
