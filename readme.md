# ads课程project1: Mini Search Engine

小组成员：刘语馨、丁雨桐、阳毓昕

## 数据结构

- Trie，用于储存word count的数据（后被废除）。
- python的dictionary及其嵌套使用，用来实现search功能。在python中，dictionary的内部数据结构为hash table，其访问、修改和插入的时间复杂度为$O(1)$。

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

  - 最后由于Trie在建立字典树时的性能太差（相比dictionary的0.95秒，Trie需要用到20-30秒），所以并没有使用

- Pretreater

  用于初步处理文本。
  
  - `__init__(self)`: [stemmer](https://pypi.org/project/snowballstemmer/)，
  - `split_file(self, file_name: str)`： 把路径是file_name的文件分成一个单词的列表，保留所有的stop words并且没有stemming
  - `phrase_indexer(self, file_name: str)`: 根据file_name路径中的文件，生成一个dictionary：{word: [locations]}， 包含了这个文件中出现过的所有单词（包括stop words，没有stemming）所在的位置
  
- Word_counter

  主要的处理器。

  - 初始化(`__init__(self)`):

    - ```python
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
      ```

  - `set_path(self, p: str)`： 设定你想要查询的文件夹（project1中是莎士比亚全集）

  - `get_all_works(self)`： 遍历path中的所有文件，并且读取其文件名到self.all_works列表中
  
  - `all_work_phrase_indexer(self)`： 遍历文件夹中的所有文件，然后生成self.indices: {word: [document_name: location]}，key是word，对应的value是另一个字典，也就是pretreater中返回的 dictionary：{word: [locations]}。

  - `word_counter(self)`：根据`self.indicies`中的内容，进行word count，并且将出现次数最多的50个单词设为stop words

  - ` search(self, text: str)`： 根据`all_work_phrase_indexer(self)`的返回值，查找一个单词或短语所在的所有文件，返回一个list，其中包含文件名。
  不会查询内容为单个stop word的词或者由3个及以下stop words组成的短语

  - `setup(self, path: str)`： 自动进行初始化、set path、get all works、生成self.indicies, word count，以便简化main函数中的调用

- main

  query入口。
  
  - `Query(wc: word_counter.word_cunter)`： 查询接口。其中唯一调用的是word counter中的serach 函数
  - `__main__`：新建一个word counter传入到query中，它是可以运行的


## 测试和结果展示

- 环境配置：python 3.11（请确保您正确设置了路径，并且在命令行工具中可以正常使用python）
- 操作步骤：
  - `cd`到目录`proj1/miniEngine/`下；
  - 在命令行运行`python main.py`或`python3 main.py`；
  - 按照提示在命令行工具中输入要查询的内容/操作。
  - 每次建立查询inverted index只需1秒左右时间，查询只需$10^{-5}$秒量级左右时间（可能因电脑性能有所偏差）。


在每个.py文件中有对应的test case，一些因为数据量过大只能用肉眼判断的并没有写上assert（偷懒了就是）
