import unittest
import naive_word_count

# 定义TrieNode，结构如下
class TrieNode:
    def __init__(self):
        self.children = dict()
        # 此处的dict是一个{char: TrieNode}的形式，表示当前TrieNode的所有children
        # 查看一个TrieNode是否有某个后继节点：print(char in TrieNode.children)
        self.isLeaf = False
        # content用来存放一个word在document中出现的次数
        # 形式为：{'document1': time1, 'document2': word2}
        self.content = dict()


    # 插入操作
    # 如果要插入的话，说明这个word在当前的Trie中是第一次出现
    # 这种情况下，tail node的dict需要初始化
    def insert_new_word(self, word: str, document_name: str, frequency: int):
        currentNode = self
        for char in word:
            if char not in currentNode.children:
                currentNode.children[char] = TrieNode()
            currentNode = currentNode.children[char]
        currentNode.isLeaf = True
        currentNode.content[document_name] = frequency


    # 查找操作
    # 如果此word存在，则返回其对应的TrieNode
    # 如果此word不存在，返回False
    def search(self, word: str):
        currNode = self
        for char in word:
            if char not in currNode.children:
                return False
            currNode = currNode.children[char]
        if currNode.isLeaf:
            return currNode

# 定义Trie，由TrieNode组成
class Trie(object):
    def __init__(self):
        # 创建新的Trie，从一个空的TrieNode开始
        self.root = TrieNode()

    def is_exist(self, word: str):
        return self.root.search(word)

    def insert(self, word: str, document_name: str, frequency: int):
        # 先进行搜索
        # 如果没有搜索到，则将此word添加进去
        # 如果搜索到了，那么不做额外的操作
        is_find = self.is_exist(word)
        if not is_find:
            self.root.insert_new_word(word, document_name, frequency)
        else :
            is_find.content[document_name] = frequency

    # 使用getRoot函数返回Trie的root
    # 最好不要直接使用Trie.root
    def getRoot(self):
        return self.root

    # Query函数，在一个Trie中查找word在document_name中出现的次数
    # 输出一个单词在每个文件中出现的次数
    def Query(self, word: str):
        is_find = self.root.search(word)
        if not is_find:
            print("This word does not exist in this Trie, please try a new one!")
        else:
            print(is_find.content)

class Test(unittest.TestCase):
    def setUp(self):
        pass

    # 测试Trie的初始化
    def test_initialize_Tire(self):
        new_trie = Trie()
        # 新的Trie应该满足：根节点的children、content都为空，并且isLeaf = False
        self.assertEquals(len(new_trie.getRoot().children), 0)
        self.assertEquals(len(new_trie.getRoot().content), 0)
        self.assertEquals(new_trie.root.isLeaf, False)

    def test_insert1(self):
        new_trie = Trie()
        document_name1 = "text1"
        word_fre1 = {'I': 1, 'love': 2, 'you': 3}
        document_name2 = "text2"
        word_fre2 = {'you': 4, 'hate': 5, 'me': 6}

        for word in word_fre1.keys():
            new_trie.insert(word, document_name1, word_fre1.get(word))
        for word in word_fre2.keys():
            new_trie.insert(word, document_name2, word_fre2.get(word))

        self.assertEquals(new_trie.is_exist('love').content.get('text1'), 2)
        self.assertEquals(new_trie.is_exist('you').content.get('text1'), 3)
        self.assertEquals(new_trie.is_exist('you').content.get('text2'), 4)
        self.assertEquals(new_trie.is_exist('hate').content.get('text2'), 5)
        self.assertEquals(new_trie.is_exist('idnotknow'), False)

    def test_Query(self):
        new_trie = Trie()
        document_name1 = "text1"
        word_fre1 = {'I': 1, 'love': 2, 'you': 3}
        document_name2 = "text2"
        word_fre2 = {'you': 4, 'hate': 5, 'me': 6}

        for word in word_fre1.keys():
            new_trie.insert(word, document_name1, word_fre1.get(word))
        for word in word_fre2.keys():
            new_trie.insert(word, document_name2, word_fre2.get(word))

        new_trie.Query('you')
        new_trie.Query('Idono')
        # 期望输出：
        # {'text1': 3, 'text2': 4}
        # This word does not exist in this Trie, please try a new one!
        # 实际上的输出：
        # {'text1': 3, 'text2': 4}
        # This word does not exist in this Trie, please try a new one!
        # pass

    def test_many_insert(self):
        new_tire = Trie()
        wc = naive_word_count.naive_word_counter()
        file_name1 = "text/test/random_word_list_1000.txt"
        file_name2 = "text/test/random_word_list_1000_copy.txt"
        document_name1 = "rw1"
        document_name2 = "rw2"
        wc.open_file(file_name1)
        wc.naive_word_count()
        for key in wc.word_count:
            new_tire.insert(key, document_name1, wc.word_count[key])
        wc.reset()
        wc.open_file(file_name2)
        wc.naive_word_count()
        for key in wc.word_count:
            new_tire.insert(key, document_name2, wc.word_count[key])
        wc.reset()
        new_tire.insert('hahaha', 'text3', 100)

        self.assertEqual(new_tire.is_exist('bite').content[document_name1], 1)
        self.assertEqual(new_tire.is_exist('mind').content[document_name2], 1)
        self.assertEqual(new_tire.is_exist('hahaha').content['text3'], 100)


if __name__ == '__main__':
    unittest.main()