import word_counter

def Query(wc: word_counter.word_cunter):
    wc.set_path('text/Shakespeare/')
    wc.get_all_works()
    wc.word_counter()
    trie = wc.new_trie
    print("欢迎在莎士比亚全集中查询您想要的内容\n")
    while True:
        word = input("请输入您想要查询的单词：")
        exist = trie.is_exist(word)
        if not exist:
            print("抱歉！无法查询到您输入的单词。如果词单词是以e结尾的，请尝试删除e之后再尽心查询。例如：查询voyag而不是voyage\n")
        else:
            print(word + "出现在以下文本中: ")
            for document_name in exist.content.keys():
                print('《' + document_name[:-4] + '》')
        is_continue = input("如果想要继续查询，请输入'yes'；如果想退出，请输入'no': ")
        if is_continue == 'no':
            break

    print("欢迎下次光临！❤️")




if __name__ == '__main__':
    wc = word_counter.word_cunter()
    Query(wc)
