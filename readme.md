# ads课程project1: Mini Search Engine

小组成员：刘语馨、丁雨桐、阳毓昕

## 数据结构

- Trie
- python的dictionary，及其嵌套使用

## project框架

- Trie(字典树)

  - Trie Node： 

    - ```
      self.children = dict()
      # 此处的dict是一个{char: TrieNode}的形式，表示当前TrieNode的所有children
      # 查看一个TrieNode是否有某个后继节点：print(char in TrieNode.children)
      self.isLeaf = False
      # content用来存放一个word在document中出现的次数
      # 形式为：{'document1': time1, 'document2': word2}
      self.content = dict()
      ```

  - 用来进行word count

  - content的信息表示的是一个term出现过的文章名字和次数

  - 在search时事用不上的

  - `is_exist(self, word: str)`： 如果这个单词不存在，返回NULL；如果存在，返回tail node。通过访问`tailnode.content`就可以查询term出现过的文章和次数

- Pretreater

  - `__init__(self)`: 定义[stop words](https://www.nltk.org/data.html) 和[stemmer](https://pypi.org/project/snowballstemmer/)，
  - `split_file(self, file_name: str)`： 把路径是file_name的文件分成一个单词的列表，保留所有的stop words并且没有stemming
  - ` filter(self, file_name: str)`：把split过后的单词列表过滤出stop words，返回一个单词列表
  - `final_stemmer(self, file_name: str)`：可以直接调用，包含了split、filter和stemming的功能，返回一个单词列表
  - `phrase_indexer(self, file_name: str)`: 根据file_name路径中的文件，生成一个dictionary：{word: [locations]}， 包含了这个文件中出现过的所有单词（包括stop words，没有stemming）所在的位置
  
- Word_counter

  - 初始化(`__init__(self)`):

    - ```python
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
          # 一个dict，用于存放搜索用的indices
          self.indices = {}
      ```

  - `set_path(self, p: str)`： 设定你想要查询的文件夹（project1中是莎士比亚全集）

  - `get_all_works(self)`： 遍历path中的所有文件，并且读取其文件名到self.all_works列表中

  - `word_counter(self)`： 生成一个新的Trie，把self.path中的所有文件都用pretreated中的`final_stemmer(self, file_name: str)`函数处理一遍，然后把信息通过trie.insert(word, document_name, freqnency)添加到Trie中

  - `all_work_phrase_indexer(self)`： 遍历文件夹中的所有文件，然后生成self.indices: {word: [document_name: location]}，key是word，对应的value是另一个字典，也就是pretreater中返回的 dictionary：{word: [locations]}。

  - ` search(self, text: str)`： 根据`all_work_phrase_indexer(self)`的返回值，查找一个单词或短语所在的所有文件，返回一个list，其中包含文件名。

  - `setup(self, path: str)`： 自动进行初始化、set path、get all works、word count，以便简化main函数中的调用

- main

  - `Query(wc: word_counter.word_cunter)`： 查询接口。其中唯一调用的是word counter中的serach 函数
  - `__main__`：新建一个word counter传入到query中，它是可以运行的


## 测试和结果展示
