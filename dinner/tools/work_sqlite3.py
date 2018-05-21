import sqlite3

class CookCursor():
    def __init__(self):
        self.cn = sqlite3.connet("D:\study\dinner\dinner\origin_data")
        self.cu = cn.cursor()

    def createTable(self,tbname,prmkey=None,**kwag):
        #TODO:传入
        
        
