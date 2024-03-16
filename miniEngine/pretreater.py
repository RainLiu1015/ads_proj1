import unittest
# https://pypi.org/project/snowballstemmer/#description snowball stemmer
# 问题：在遇到任何以e结尾的单词时，stemmer都会将其词尾的e去除，这一点在query的时候要注意
import snowballstemmer
import re

class pretreater:
    def __init__(self):
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
        # 唯一的问题，Porter Stemmer的精确度确实不够……对过去式的stemming非常之差
        self.stemmer = snowballstemmer.stemmer('english')

    # 这个函数将会处理单个文件，将.txt文件中的内容进行分句和分词，最后传回一个word的list
    # python的list最多能容纳2^64-1个元素，所以不用担心超了的问题！（应该
    def split_file(self, file_name: str):
        word_list = []
        pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|#|\$|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）|\n'
        with open(file_name, encoding='gb18030', errors='ignore') as f:
            for line in f:
                line = line.lower()
                first_splited = re.split(pattern, line)
                for word in first_splited:
                    if word != '':
                        word_list.append(word)

        return word_list

    def filter(self, file_name: str):
        word_list = self.split_file(file_name)
        filtered_words = []
        for word in word_list:
            if not word in self.stop_words:
                filtered_words.append(word)
        return filtered_words

    def final_stemmer(self, file_name: str):
        word_list = self.filter(file_name)
        stemmed_word = []
        for word in word_list:
            word = self.stemmer.stemWord(word)
            stemmed_word.append(word)
        return stemmed_word

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
                word = u''.join(current_word).lower()
                word_list.append((word_index, word))
                current_word = []
        if current_word:
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
        file_name = 'G:/P1/miniEngine/text/small_test/sentence_test.txt'
        print(pre.split_file(file_name))

    def test_split_long(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/Shakespeare/AsYouLikeIt.txt'
        print(pre.split_file(file_name))

    def test_filter_short(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/small_test/sentence_test.txt'
        print(pre.filter(file_name))

    def test_filter_long(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/Shakespeare/AsYouLikeIt.txt'
        print(pre.filter(file_name))

    def test_stemmer_short(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/small_test/sentence_test.txt'
        print(pre.final_stemmer(file_name))

    def test_stemmer_long(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/Shakespeare/AsYouLikeIt.txt'
        print(pre.final_stemmer(file_name))

    def test_phrase_spliter_short(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/small_test/sentence_test.txt'
        print(pre.phrase_spliter(file_name))

    def test_phrase_spliter_long(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/Shakespeare/AsYouLikeIt.txt'
        print(pre.phrase_spliter(file_name))
        # 至少证明了一点，处理起一个文件来还是很快速的

    def test_phrase_indexer_short(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEnginetext/small_test/sentence_test.txt'
        result = pre.phrase_indexer(file_name)
        self.assertEqual(len(result.get('plays')), 1)
        self.assertEqual(len(result.get('example')), 1)

    def test_phrase_indexer_medium(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEnginetext/small_test/fragment.txt'
        result = pre.phrase_indexer(file_name)
        self.assertEqual(len(result.get('you')), 3)
        self.assertEqual(len(result.get('to')), 4)

    def test_phrase_indexer_long(self):
        pre = pretreater()
        file_name = 'G:/P1/miniEngine/text/Shakespeare/Hamlet.txt'
        result = pre.phrase_indexer(file_name)
        self.assertEqual(len(result.get('francisco')), 10)
        self.assertEqual(len(result.get('prince')), 9)
        self.assertEqual(len(result.get('sadness')), 1)
        self.assertEqual(len(result.get('queen')), 119)
        # Ran 1 test in 0.066s, test pass