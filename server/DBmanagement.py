import pymysql
from passlib.hash import pbkdf2_sha256
class Management:
    def __init__(self,h,u,p):
        self.conn = pymysql.connect(host=h, user=u, password=p, db='hunet', charset='utf8')

    #사용자 추가
    def add_user(self,id,pwd):
        cur = self.conn.cursor()
        cur.execute("""select * from manager where id = %s;""",id)
        
        if cur.fetchone() == None:
            pwd = hash_password(pwd)
            cur.execute("""insert into manager (id, pwd) values (%s,%s);""",(id,pwd))
            self.conn.commit()
            return True
        return False
   
        
    #사용자 확인(db_manager가 비었는지 확인, 비었으면 True) 
    def check_user(self):
        cur = self.conn.cursor()
        cur.execute("""select pwd from manager;""")
        a = cur.fetchone()
        if a == None:
            return True
        return False


    # 로그인 확인
    def login(self,id,pwd):
        cur = self.conn.cursor()
        cur.execute("""select pwd from manager where id = %s;""",id)
        a = cur.fetchone()
        if(check_password(pwd,a[0])):
            return True
        else :
            return False

    

    # rtsp:

    # 등록
    def rtsp_add(self,name,address,rtsp_limit):
        cur = self.conn.cursor()
        cur.execute("""select count(*) from rtsp""")
        num = cur.fetchone()
        if num[0] >= rtsp_limit:
            return (False,1)
        cur.execute("""select * from rtsp where ip_address = %s;""",address)
        if cur.fetchone() == None:
            query = """insert into rtsp (name, ip_address) values (%s, %s);"""
            values = (name,address)
            cur.execute(query,values)
            self.conn.commit()
            last_id = cur.lastrowid
            new_entry = {"id": last_id, "name": name, "ip_address": address}
            return (True,new_entry)
        
        return (False,0)

    # 삭제
    def rtsp_delete(self,num):
        cur = self.conn.cursor()
        query = """delete from rtsp where id = %s;"""
        cur.execute(query,num)
        self.conn.commit()

    # 읽기
    def rtsp_get(self):
        cur = self.conn.cursor()
        cur.execute("""select * from rtsp;""")
        return cur.fetchall()

    # 이메일:

    # 추가
    def email_add(self,email):
        cur = self.conn.cursor()
        cur.execute("""select * from email where address = %s""",email)
        if cur.fetchone() == None:
            query = """insert into email (address) values (%s);"""
            cur.execute(query,email)
            self.conn.commit()
            return True
        return False

    # 확인
    def email_get(self):
        cur = self.conn.cursor()
        cur.execute("""select * from email;""")
        return cur.fetchall()

    # 삭제
    def email_delete(self, num):
        cur = self.conn.cursor()
        query = """delete from email where id = %s;"""
        cur.execute(query, num)
        self.conn.commit()
    
    def refresh_connection(self,h,u,p):
        self.conn.close()
        self.__init__(h,u,p)

def hash_password(original_pwd):
    key = 'hunet'
    pwd = original_pwd + key
    pwd = pbkdf2_sha256.hash(pwd)
    return pwd

def check_password(original_pwd,hashed_pwd):
    salt = 'hunet'
    check = pbkdf2_sha256.verify(original_pwd + salt,hashed_pwd)
    return check