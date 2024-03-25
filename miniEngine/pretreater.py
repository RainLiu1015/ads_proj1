import unittest
"""
snowball stemmer来自于 https://pypi.org/project/snowballstemmer/#description
Author：snowball-discuss@lists.tartarus.org
"""
import snowballstemmer
import re

class pretreater:
    def __init__(self):
        # 将porter stemmer改为了snowball stemmer，相对更加精准一点
        self.stemmer = snowballstemmer.stemmer('english')

    # 这个函数将会处理单个文件，将.txt文件中的内容进行分句和分词，最后传回一个word的list
    # python的list最多能容纳2^64-1个元素，所以不用担心超了的问题！（应该
    def split_file(self, file_name: str):
        word_list = []
        pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|#|\$|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）|\n'
        # 选择编码方式为gb18030，适配更多硬件；忽略error，防止运行时报错
        with open(file_name, encoding='gb18030', errors='ignore') as f:
            for line in f:
                line = line.lower() # 忽略大小写
                first_splited = re.split(pattern, line) # 以pattern中的所有符号为分割
                for word in first_splited:
                    if word != '':
                        word_list.append(word)

        return word_list

    """
    这里的spliter和接下来的phrease indexer的思路借鉴了来自 https://blog.csdn.net/u014328357/article/details/49943037 的CSDN博客
    原博主为： @玉儿Qi
    个人主页网站：https://blog.csdn.net/u014328357?type=blog
    因为是借鉴的，所以有些数据结构和原文件有不匹配的地方，同时产生了部分数据的冗余
    （譬如其实word_list中的元素是tuple，但是在此project的后面部分只用到了tuple中的word，并没有用到id这个属性）
    这是本project的不足之处之一，待有空将会逐步修改精简
    """
    def phrase_spliter(self, file_name: str):
        word_list = []
        word_index = 0
        current_word = self.split_file(file_name)
        for word in current_word:
            word_list.append((word_index, word))
            word_index += 1

        return word_list

    # 上面这个函数只能用来处理file，但是如果要处理phrase，就需要phrase_spliter_for_words
    def phrase_spliter_for_words(self, text: str):
        word_list = []
        current_word = []
        word_index = 0
        for i, c in enumerate(text):
            if c.isalnum():
                current_word.append(c)
            elif current_word:
                word_index += 1
                word = u''.join(current_word).lower() # 忽略大小写
                word_list.append((word_index, word))
                current_word = []
        if current_word: # 如果current word不为空的话
            word_index += 1
            word = u''.join(current_word).lower()
            word_list.append((word_index, word))

        return word_list

    # 这个函数用于在某个特定文件中这样的dict：{word: [locations]}
    # 即这个word在这个file_name对应的file中在哪些地方出现了
    def phrase_indexer(self, file_name: str):
        inverted = {}

        for index, word in self.phrase_spliter(file_name):
            # 设定location的dict格式
            locations = inverted.setdefault(word, [])
            locations.append(index)

        return inverted

class Test(unittest.TestCase):
    def test_split_short(self):
        pre = pretreater()
        file_name = 'text/small_test/sentence_test.txt'
        print(pre.split_file(file_name))

    def test_split_long(self):
        pre = pretreater()
        file_name = 'text/Shakespeare/AsYouLikeIt.txt'
        print(pre.split_file(file_name))

    # def test_filter_short(self):
    #     pre = pretreater()
    #     file_name = 'text/small_test/sentence_test.txt'
    #     print(pre.filter(file_name))

    # def test_filter_long(self):
    #     pre = pretreater()
    #     file_name = 'text/Shakespeare/AsYouLikeIt.txt'
    #     print(pre.filter(file_name))

    def test_phrase_spliter_short(self):
        pre = pretreater()
        file_name = 'text/small_test/sentence_test.txt'
        print(pre.phrase_spliter(file_name))

    def test_phrase_spliter_long(self):
        pre = pretreater()
        file_name = 'text/Shakespeare/AsYouLikeIt.txt'
        print(pre.phrase_spliter(file_name))
        # 至少证明了一点，处理起一个文件来还是很快速的

    def test_phrase_indexer_short(self):
        pre = pretreater()
        file_name = 'text/small_test/sentence_test.txt'
        result = pre.phrase_indexer(file_name)
        self.assertEqual(len(result.get('plays')), 1)
        self.assertEqual(len(result.get('example')), 1)

    def test_phrase_indexer_medium(self):
        pre = pretreater()
        file_name = 'text/small_test/fragment.txt'
        result = pre.phrase_indexer(file_name)
        self.assertEqual(len(result.get('you')), 3)
        self.assertEqual(len(result.get('to')), 4)

    def test_phrase_indexer_long(self):
        pre = pretreater()
        file_name = 'text/Shakespeare/Hamlet.txt'
        result = pre.phrase_indexer(file_name)
        self.assertEqual(len(result.get('francisco')), 10)
        self.assertEqual(len(result.get('prince')), 9)
        self.assertEqual(len(result.get('sadness')), 1)
        self.assertEqual(len(result.get('queen')), 119)
        # Ran 1 test in 0.066s, test pass

if __name__ == '__main__':
    unittest.main()