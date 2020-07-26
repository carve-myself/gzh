import pymysql


class DBUtil():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 3306
        self.user = 'root'
        self.password = '123456'
        self.db = 'gzh'

    # 打开数据库连接
    def getConnect(self):
        return pymysql.connect(self.host, self.user, self.password, self.db)

    # 根据dict插入一条数据
    def insertOne(self, data_dict, table_name):
        global insert_sql
        conn = self.getConnect()

        keyStr = ''  # 列的字段
        valueStr = ''  # 行字段
        for key in data_dict:
            keyStr += ' ' + key + ','
            valueStr = valueStr + "%(" + key + ")s,"
        keyStr = keyStr.rstrip(',')
        valueStr = valueStr.rstrip(',')

        try:
            cursor = conn.cursor()
            insert_sql = "insert into " + table_name + "(" + keyStr + ") values(" + valueStr + ")"
            result = cursor.execute(insert_sql, data_dict)
            conn.commit()
            cursor.close()
            conn.close()
            # print("插入单条数据成功,影响行数:", result)
        except Exception as e:
            conn.rollback()
            print("插入单条操作失败:", e)
            print(insert_sql)

    # 查询数据
    def select(self, sql):
        conn = self.getConnect()
        cur = conn.cursor()
        try:
            # 执行SQL语句
            cur.execute(sql)
            conn.commit()
            # 获取所有记录列表
            results = cur.fetchall()
            return results
        except:
            print("Error: unable to fecth data")
        cur.close()
        conn.close()
