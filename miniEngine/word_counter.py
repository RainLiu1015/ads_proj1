import Trie
import os
import unittest
import pretreater
import snowballstemmer

class word_cunter:
    def __init__(self):
        # 一个dict，用来存放文件夹Shakespeare下的所有txt文件的文件名，并生成对应的id
        self.all_works = {}
        # 一个int，用来记录Shakespeare文件夹下的文件总个数
        self.num_document = 0
        # 一个string，用来存放Shakespeare文件夹的相对路径
        self.path = ''
        # 一个list，用来存放所有的stop words
        self.stop_words = []
        # 一个pretreater, 包含了split，filter，stemmer等组件
        self.pre = pretreater.pretreater()
        # 一个dict，用于存放搜索用的indices
        self.indices = {}
        # 一个dict，用来记录term出现的总次数
        self.count = {}
        # stemmer
        self.stemmer = snowballstemmer.stemmer('english')

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
        for word in self.indices:
            sum = 0
            for file_name in self.indices[word]:
                sum += len(self.indices[word][file_name])
            word = self.stemmer.stemWord(word) # 经过了stemming之后再加入count中
            if word not in self.count:
                self.count[word] = sum
            else :
                self.count[word] += sum
        for i in range(50): #将出现次数最多的50个单词设为stop words
            curr_word = max(self.count, key=lambda x: self.count[x])
            self.stop_words.append(curr_word)
            print('单词', curr_word , '出现了', self.count[curr_word], '次，设为stop wrod')
            self.count.pop(curr_word)

    """
    建立一个invered index,形式为{word: {document_name: [locations]}}
    """
    def all_work_phrase_indexer(self):
        indices = {}
        for work_name in self.all_works:
            file_name = self.path + work_name
            inverted = self.pre.phrase_indexer(file_name)
            for word in inverted.keys():
                word_s = self.stemmer.stemWord(word)
                if word_s in indices:
                    indices[word_s][work_name] = inverted[word]
                else :
                    indices[word_s] = {}
                    indices[word_s][work_name] = inverted[word]
        self.indices = indices

    """
    定义一个可以搜索word/phrase在哪些文件里的函数
    主要利用的是self.indices: {word: {document_name: location}}这样一个dict
    """
    def search(self, text: str):
        words_tuple = self.pre.phrase_spliter_for_words(text)
        result = []
        # for word in words:
        #     print(word[1])  words是一个由tuple(int, word)组成的list
        if (len(words_tuple) == 1): # 此时是一个单词
            word = words_tuple[0][1]
            word = self.stemmer.stemWord(word)
            if (word in self.stop_words):
                print('您查询的是一个stopword，请重新输入！')
                return result
            if word not in self.indices.keys():
                return result
            else:
                for document_name in self.indices.get(word).keys():
                    result.append(document_name)
        else: # 此时是一个短语
            # 判断是否是3个及一下的stop word组成的，如果是，则不予搜索
            if all(self.stemmer(tuple[1]) in self.stop_words for tuple in words_tuple) and len(words_tuple) <= 3:
                print('您输入的是三个及以下的stop words组成的短语，请重新输入！')
                return result
            # 先得到第一个word的locatons
            first_word = words_tuple[0][1]
            first_word = self.stemmer.stemWord(first_word)
            if first_word not in self.indices.keys():
                return []
            final_locations = self.indices.get(first_word).copy()
            # 如果第一个word都找不到的话，肯定就返回空了
            if len(final_locations) == 0:
                return []
            #接下来用排除法
            for i in range(1, len(words_tuple)):
                curr_word = words_tuple[i][1]
                curr_word = self.stemmer.stemWord(curr_word)
                if curr_word not in self.indices.keys():
                    return []
                curr_locations = self.indices.get(curr_word).copy()
                # curr_locations = {document_name: [locations]}
                if len(curr_locations) == 0:
                    return []
                # 第一次排除：如果当前单词和前一个单词没有出现在同一个文件里，则将这个文件移除
                for document_name in list(curr_locations.keys()):
                    if document_name not in final_locations.keys():
                        del curr_locations[document_name]
                    if len(curr_locations) == 0:
                        return [] #如果经过第一次排除，curr_locations就为空，那么返回空
                # 第二次排除：在所有前一个单词和当前单词都出现过了的文件里，他们两个要连续出现过至少一次
                for document_name in list(curr_locations.keys()):
                    locations1 = final_locations.get(document_name)
                    locations2 = curr_locations.get(document_name)
                    locations1 = [x + 1 for x in locations1] # 将locations1中的所有location都加1，得到后继位置
                    locations2 = list(set(locations1) & set(locations2)) # 将后继位置和现有的locations2求交集
                    if len(locations2) == 0:
                        if document_name in curr_locations.keys():
                            del curr_locations[document_name]
                        if len(final_locations) == 0 or len(curr_locations) == 0:
                            return []
                    else :
                        curr_locations[document_name] = locations2
                    # 更新，将final_locations改为curr_location经过两轮排除后剩下的值，
                    # final locations的长度在运算中应该不断缩短，这样也使得后期运算不会太慢
                final_locations = curr_locations
            for document_name in final_locations.keys():
                result.append(document_name)
        return result

    def setup(self, path: str):
        print('正在定位到莎士比亚全集……')
        self.set_path(path)
        print('定位完成，正在扫描作品……')
        self.get_all_works()
        print('正在建立inverted index……')
        self.all_work_phrase_indexer()
        print('正在建立进行word count并设定stop words……')
        self.word_counter()
        print('设置完成。enjoy！')

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


# 这种数据量巨大且未知结果的模块，只能人眼测试了（汗
    def test_word_count_large(self):
        wc = word_cunter()
        wc.set_path('text/Shakespeare_small_test/')
        wc.get_all_works()
        wc.all_work_phrase_indexer()
        wc.word_counter()

    def test_phrase_indexer_small(self):
        wc = word_cunter()
        wc.set_path('text/small_test/')
        wc.get_all_works()
        wc.all_work_phrase_indexer()
        print(wc.indices)
        # 人工比对，测试通过

    def test_phrase_indexer_large(self):
        wc = word_cunter()
        wc.set_path('text/Shakespeare_small_test/')
        wc.get_all_works()
        wc.all_work_phrase_indexer()
        print(wc.indices)
        # Ran 1 test in 0.083s，测试通过

    def test_phrase_spliter(self):
        wc = word_cunter()
        wc.search('to be or not to be')

    def test_search_single_word(self):
        wc = word_cunter()
        wc.set_path('text/Shakespeare_small_test/')
        wc.get_all_works()
        wc.all_work_phrase_indexer()
        self.assertEqual(wc.search('hamlet'), ['Hamlet.txt'])
        self.assertEqual(wc.search('be').sort(), ['Hamlet.txt', 'Fake.txt'].sort())
        self.assertEqual(wc.search('kiss'), ['LovesLaboursLost.txt'])

    def test_search_phrase_small(self):
        wc = word_cunter()
        wc.set_path('text/Shakespeare_small_test/')
        wc.get_all_works()
        wc.all_work_phrase_indexer()

        self.assertEqual(wc.search('to be or not to be'), ['Hamlet.txt'])
        self.assertEqual(wc.search('that is the question'), ['Hamlet.txt'])
        self.assertEqual(wc.search('To die, to sleep'), ['Hamlet.txt'])
        self.assertEqual(wc.search('fake file'), ['Fake.txt'])
        self.assertEqual(wc.search('drink wine'), [])

if __name__ == '__main__':
    unittest.main()