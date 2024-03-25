import word_counter
import time

def Query(wc: word_counter.word_cunter):
    print("欢迎在莎士比亚全集中查询您想要的内容")
    print("正在加载中，这将需要一段时间……\n")
    start = time.time()
    wc.setup('text/Shakespeare/')
    end = time.time()
    print('建立inverted index共用了', str(end - start)[:4], 's')
    while True:
        text = input("请输入你要查询的单词或短语，退出请输入q:")
        if (text == 'q'):
            break
        start_search = time.time()
        result = wc.search(text)
        end_search = time.time()
        if result == []:
            print("抱歉！没有找到你需要的单词或短语QAQ\n")
            continue
        else:
            print(text + ' 出现在以下作品中：')
            for document_name in result:
                print('《' + document_name[:-4] +'》')
            print('\n')
        print('此次查询用时', str(end_search - start_search)[:4], str(end_search - start_search)[17:], 's')

    print("欢迎下次光临！❤️")




if __name__ == '__main__':
    wc = word_counter.word_cunter()
    Query(wc)
