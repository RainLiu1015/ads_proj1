# Project1

### 题目要求：

```
In this project, you are supposed to create your own mini search engine which can handle inquiries over “The Complete Works of William Shakespeare” (http://shakespeare.mit.edu/).

You may download the functions for handling stop words and stemming from the Internet, as long as you add the source in your reference list.

Your tasks are:
(1) Run a word count over the Shakespeare set and try to identify the stop words (also called the noisy words) – How and where do you draw the line between “interesting” and “noisy” words?
(2) Create your inverted index over the Shakespeare set with word stemming. The stop words identified in part (1) must not be included.
(3) Write a query program on top of your inverted file index, which will accept a user-specified word (or phrase) and return the IDs of the documents that contain that word.
(4) Run tests to show how the thresholds on query may affect the results.


Grading Policy:
Programming: Write the programs for word counting (1 pt.), index generation (5 pts.) and query processing (3 pts.) with sufficient comments.

Testing: Design tests for the correctness of the inverted index (2 pts.) and thresholding for query (2 pts.). Write analysis and comments (3 pts.). Bonus: What if you have 500 000 files and 400 000 000 distinct words? Will your program still work? (+2 pts.)

Documentation: Chapter 1 (1 pt.), Chapter 2 (2 pts.), and finally a complete report (1 point for overall style of documentation).

Note: Anyone who does excellent job on answering the Bonus question will gain extra points.
```

[莎士比亚全集repo，但是是html版](https://kkgithub.com/TheMITTech/shakespeare)

[来自Kaggle的dataset](https://www.kaggle.com/datasets/kewagbln/shakespeareonline)

## 1 知识储备 & 整理

### 1.1 Makefile

个人感觉写得超级好的Makefile教程->[指路知乎](https://zhuanlan.zhihu.com/p/618350718)

反正最后只要一个人写就行了（

### 1.2 Stemming和stop words

- 在往年（指4年前，汗）的[project](https://kkgithub.com/haoliu97/mini-search-engine.git)中找到的被引用的stemmer：[porter2_stemmer](https://kkgithub.com/smassung/porter2_stemmer/tree/master/util)， 既然有人用过说明是确实可以用的！但是唯一的问题就是，这个文件适配C++而不是C。在github上找到的可以用的现成stemmer有：

  - [snowball stmmer](https://kkgithub.com/snowballstem/snowball)，GitHub上🌟最多的，但是小人实在看不懂

  - [porter stemmer](https://kkgithub.com/wooorm/stmr.c)，轻量，用起来很方便，直接`#include "stmr.h"`即可，具体表现不清楚。我自己在C里面试了一下，可以直接调用

    - ```C
      #include <stdio.h>
      #include <string.h>
      #include "stmr.h"
      
      
      int main(int argc, const char * argv[]) {
          // insert code here...
          char w[20] = "stopped";
          char *word = w;
          int end = stem(word, 0, strlen(word) - 1);
          word[end + 1] = 0;
          printf("%s\n", word);
          return 0;
      }
      //输出：stop
      ```

    - 

  - [snowball stemmer](https://kkgithub.com/tebeka/snowball)，比较复杂，可能表现会稍微好一点？但是感觉调用比较麻烦（我看不懂）：

    - ```c
      package snowball_test
      
      import (
      	"fmt"
      
      	"github.com/tebeka/snowball"
      )
      
      func Example() {
      	stemmer, err := snowball.New("english")
      	if err != nil {
      		fmt.Println("error", err)
      		return
      	}
      	defer stemmer.Close()
      
      	fmt.Println(stemmer.Stem("worked"))
      	fmt.Println(stemmer.Stem("working"))
      	fmt.Println(stemmer.Stem("works"))
      	// Output:
      	// work
      	// work
      	// work
      }
      ```

  - 还有一些ruby stemmer，感觉不是很懂，似乎不是给我们这种小白用的

  - Stemmer for python，python作为备选语言，我也找了一些stemmer

    - [porter2](https://kkgithub.com/mdirolf/pyporter2)

    - 调用代码：

      ```python
      if __name__ == '__main__':
          word = 'wolves'
          # print(stemmer.PorterStemmer().stem('ourselves'))
          print(Porter2Stemmer.Stemmer('english').stemWord('consistant'))
      ```

    - 但是大多数porter2 stemmer都有一个问题：不能将-ves类型stem成正常类型。也就是'wolves'和'wolf'不能抽象到一个单词。但是根据stemming的定义，甚至他们可能不需要变成同一个单词（毕竟复数和单数本就不是一个意思对吗？）
    
    - python自带库[NLTK](https://www.cnblogs.com/Patrick-L/p/12251747.html)，可以直接进行忽略stop words + stemming的操作，有多种stemming算法（porter / snowball）可以选择：
    
      ```python
      >>> from nltk.stem.snowball import SnowballStemmer
      >>> print(" ".join(SnowballStemmer.languages))
      danish dutch english finnish french german hungarian italian
      norwegian porter portuguese romanian russian spanish swedish
      
      >>> stemmer = SnowballStemmer("english")
      >>> print(stemmer.stem("running"))
      run
      
      >>> stemmer2 = SnowballStemmer("english", ignore_stopwords=True)
      >>> print(stemmer.stem("having"))
      have
      >>> print(stemmer2.stem("having"))
      having
      
      >>> print(SnowballStemmer("english").stem("generously"))
      generous
      >>> print(SnowballStemmer("porter").stem("generously"))
      gener
      ```
    
    - 在安装nltk和`nltk.download('stopwords')`时遇到了一些问题，解决方法[参考此博客](https://blog.csdn.net/qq_45571138/article/details/121064447). 但是这个snowball亲测不好用……第一，`ignore_stopword = True`，但是屁用没有；第二，nltk包内容是不可见的，也就意味着我们不能修改函数的细节，智能顺应包的规范；
    

- stop words, GitHub上有很多英语stop words的现成表格

  - [很多不同标准的英语stopwords表](https://kkgithub.com/stopwords-iso/stopwords-en)
  - 但是问题在于“How and where do you draw the line between “interesting” and “noisy” words?”，例如"to be or not to be"。我查了网上，似乎也没什么好的解决办法……
  - 大家基本上选择直接将停用词删除

- python配置有现成的NLTK（自然语言工具包）可以处理删除停用词，直接调用即可：

  ```python
  from nltk.corpus import stopwords 
  from nltk.tokenize import word_tokenize 
  
  example_sent = "This is a sample sentence, showing off the stop words filtration."
  
  stop_words = set(stopwords.words('english')) 
  
  word_tokens = word_tokenize(example_sent) 
  
  filtered_sentence = [w for w in word_tokens if not w in stop_words] 
  
  print(word_tokens) 
  print(filtered_sentence) 
  
  # 输出：
  # ['This', 'is', 'a', 'sample', 'sentence', ',', 'showing', 'off', 'the', 'stop', 'words', 'filtration', '.']
  # ['This', 'sample', 'sentence', ',', 'showing', 'stop','words', 'filtration', '.']
  # 参考博客：https://blog.csdn.net/miaoxiaowuseng/article/details/107343427
  ```

### 1.3 Word Count

WordCount是一种常见的文本处理任务，用于计算给定文本中单词的数量。它可以用于统计文章、报告或其他文档中单词的出现频率。

### 1.3.1 用什么语言

- python在处理字符串方面具有很良好的性质，结构也更加简单

  - 短短一段代码就可以实现word count的功能；

    ```python
    def word_count(text):
        # 将文本转换为小写，并将标点符号替换为空格
        text = text.lower().replace(",", " ").replace(".", " ").replace("!", " ").replace("?", " ")
     
        # 利用空格将文本分割成单词列表
        words = text.split()
     
        # 创建一个空字典，用于存储每个单词的计数
        word_count = {}
     
        # 遍历单词列表，统计每个单词的出现次数
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
     
        return word_count
     
    # 示例用法
    text = "This is a sample sentence. This sentence is used for word count example."
    result = word_count(text)
    print(result)
    print(result.keys())
    print(result.get('this'))
    print(result.popitem())
    
    #{'this': 2, 'is': 2, 'a': 1, 'sample': 1, 'sentence': 2, 'used': 1, 'for': 1, 'word': 1, 'count': 1, 'example': 1}
    #dict_keys(['this', 'is', 'a', 'sample', 'sentence', 'used', 'for', 'word', 'count', 'example'])
    #2
    #('example', 1)
    ```

  - python文件之间的相互引用比较方便，一个`import`即可搞定，不存在是否需要按顺序编译的情况，如果是在同级目录下甚至不用考虑路径问题；

  - python可以直接使用大量的NLP（Natural Language Process，自然语言处理）库，通过下载后`import`即可访问，有些自动有判断stopwords的功能；

  - Python的dictionary结构功能非常齐全，具体功能包括但不限于：

    - 可以直接根据key（字符串）搜索对应的value（数值）: `.get('key')`

    - 直接得到所有keys的集合: `.keys()`

    - dict + for，可以直接完成word count的叠加

      ```python
      for k in result.keys():
        tries[k] += result.get(k)
      ```

  - python 中的test写起来比较方便，不需要单独的文件存放，当然也不需要指定编译顺序。一个典型python测试文件的写法如下：

    ```python
    class A:
      # 定义函数
    	def func(self, var1, var2, ...):
        ...
        return ...
      
      # 定义test，这个函数是可以直接运行的
      def func_test(self):
        self.assertEqual(func(a, b), expected_output) #如果两边不相等，test会报错，能清楚看到哪个case错了
    ```

    一个文件中可以编写多个test function，大量测试。

- C，除了咱们掌握的比较熟练，我想不出来有什么特别的优势……C本身不支持string类型，在文本处理时难免会遇到通篇都是指针的情况。而指针……dddd，比较容易出错、难以管理
  - 如果要使用C的话，word parse肯定需要单独一个函数



## 2. 数据结构 & 工程架构

### 2.1 数据结构

- **用什么数据结构存放terms？**这显然是一个非常好的问题。
  - 树
    
  - 动态hash table
    - 在hash code分配得足够平均的情况下，可以使得插入和删除的复杂度为$O(1)$（您猜怎么着，python里正好有直接生成hashcode的函数呢！）
    
  - tries
  - python字典

​	我个人最推荐Tire（字典树）（这名字一听就是为了处理文本设计的！！不是么？？！）

​	来自[wiki的字典树](https://oi-wiki.org/string/trie/)，包含了字典树的生成、查询等代码（仅有C++与Python版本）

```python
class trie:
    def __init__(self):
        self.nex = [[0 for i in range(26)] for j in range(100000)]
        self.cnt = 0
        self.exist = [False] * 100000  # 该结点结尾的字符串是否存在

    def insert(self, s):  # 插入字符串
        p = 0
        for i in s:
            c = ord(i) - ord('a')
            if not self.nex[p][c]:
                self.cnt += 1
                self.nex[p][c] = self.cnt  # 如果没有，就添加结点
            p = self.nex[p][c]
        self.exist[p] = True

    def find(self, s):  # 查找字符串
        p = 0
        for i in s:
            c = ord(i) - ord('a')
            if not self.nex[p][c]:
                return False
            p = self.nex[p][c]
        return self.exist[p]
```

​	如果使用字典树，可以完成很多extra的功能：查询拥有同样prefix的terms等。



- **用什么结构存放inverted index？**

  每个term对应的inverted index，该如何和term联系在一起？

  - python自带的dictionary类型可以实现这样的结构：

    ```python
    			#             A
          #           /    \
          #          D      P
          #         / \
          #        D   A    此处D、A为尾节点
          #        |   |
          # dict{'document1': time1, 'document2': time2, ...}
    ```

    - 如果只要实现word count，我们甚至可以不用特定的数据结构储存terms，直接使用`dict{'term1', dict{'document1.1', time1.1, 'document1.2', time1.2, ...}, 'term2', dict{'document2.1', time2.1, 'document2.2', time2.2, ...}, ...}`这样字典里面套字典的结构进行储存（God这会有多么方便！）

  - 链表

  - 数组

### 2.2 工程架构 - 应该有几个文件？分别实现怎样的功能？

- document parse
  - 将大量的文件/很大的单个文件按照document name分成可以直接给pretreat处理的格式，比如按照自然段分割、按照句子分割、按照单词分割等
    - [python英文分句，段落->句子](https://blog.csdn.net/weixin_39450145/article/details/112973381)
    - [python英文分局，句子->单词](https://blog.csdn.net/weixin_44749822/article/details/124740549)
    - [python读取一个文件夹中的所有文件](https://blog.csdn.net/LZGS_4/article/details/50371030)
    - [python读取一个文件夹中所有文件的文件名](https://blog.csdn.net/zhuzuwei/article/details/79925562)
  - document parse的具体步骤应该是：
    1. 先读取莎士比亚全集文件夹下的所有文件名，做成一个dict，这样可以根据文件名查询到文件id：`{document_name: id}`
    2. 再遍历dict，用word_counter处理每个文件，同时进行pretreat、将terms加入trie
  - 返回一个可以直接传给pretreat处理的数据结构
- pretreat(stemming & stopwords)
  - 用stopword功能去除所有stopwords
  - 用stemming将所有的单词词干提取
  - 这一步应该返回的是单词的集合
- word count & index generation
  - 储存term的数据结构应该在这一部分完成
  - 利用上一步返回的单词的集合，进行word count
  - 如果word count返回一个dictionary，就可以直接进行index generation
  - 返回一个dict/trie/whatever...
- Query
  - 前几个文件的内容是编写函数和test case，这个文件的作用是调用和返回结果（理论上来说前面几个文件可以没有任何输出）
  - 将所有前面的文件import进来
  - `parsed = document_parse('./shakespera.txt')`， `pretreated = pretreat(parsed)`， `result = wordcount_indexgen(pretreated)`， `find(result, 'term')`。
  
  ```
  import pretreat
  import word_count
  
  Tire = word_count(pretreat('./shakepeara.txt'))
  input = 用户输入的单词
  if (Trie.find(intput) = True):
  	return Trie.get(intput).keys()
  else :
  	print('此单词不存在')
  ```
  
  

