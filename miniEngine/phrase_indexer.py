import pretreater

class phrase_indexer:
    def __init__(self):
        #一个pretreater，用来实现split等功能
        self.pre = pretreater.pretreater()
        # 一个path，此工程中默认是'/text/Shakespeare/'
        self.path = ''
        # 一个dict，用来存放所遇到的短语和对应的文件名
        # 虽然我很担心dict的查询速度和容量大小，但是事到如今，硬着头皮也得上了
        # 上吧！dictionary！
        inverted = {}
        # 一个list，用来存放文件夹下所有文件的