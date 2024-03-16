import word_counter

def Query(wc: word_counter.word_cunter):
    print("欢迎在莎士比亚全集中查询您想要的内容")
    print("正在加载中，这将需要一段时间……\n")
    wc.setup('text/Shakespeare/')
    while True:
        text = input("请输入你要查询的单词或短语，退出请输入q:")
        if (text == 'q'):
            break
        result = wc.search(text)
        if result == []:
            print("抱歉！没有找到你需要的单词或短语QAQ")
            continue
        else:
            print(text + ' 出现在以下作品中：')
            for document_name in result:
                print('《' + document_name[:-4] +'》')

    print("欢迎下次光临！❤️")




if __name__ == '__main__':
    wc = word_counter.word_cunter()
    Query(wc)
