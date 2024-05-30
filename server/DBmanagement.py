import pymysql

class Management:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='hunet', charset='utf8')
        
    #로그인 확인
    def login(self,id,pwd):
        cur = self.conn.cursor()
        cur.execute("""select pwd from manager where id = %s;""",id)
        a = cur.fetchone()
        if(a[0] == pwd):
            return True
        else :
            return False
    
    #rtsp:

    #등록
    def rtsp_add(self,name,address):
        cur = self.conn.cursor()
        query = """insert into rtsp (name, ip_address) values (%s, %s);"""
        values = (name,address)
        cur.execute(query,values)
        self.conn.commit()

        # last_id = cur.fetchone()[0]
        # new_entry = {"id": last_id, "name": name, "ip_address": address}

        # return new_entry

    #삭제
    def rtsp_delete(self,num):
        cur = self.conn.cursor()
        query = """delete from rtsp where id = %s;"""
        cur.execute(query,num)
        self.conn.commit()
        
    #읽기
    def rtsp_get(self):
        cur = self.conn.cursor()
        cur.execute("""select * from rtsp;""")
        return cur.fetchall()

    #이메일 
    #추가
    def email_add(self,email):
        cur = self.conn.cursor()
        query = """insert into email (address) values (%s);"""
        cur.execute(query,email)
        self.conn.commit()
    
    #확인
    def email_get(self):
        cur = self.conn.cursor()
        cur.execute("""select * from email;""")
        return cur.fetchall()
    
    #삭제
    def rtsp_delete(self,num):
        cur = self.conn.cursor()
        query = """delete from email where id = %s;"""
        cur.execute(query,num)
        self.conn.commit()


    
       
        








