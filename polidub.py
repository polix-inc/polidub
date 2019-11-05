import sqlite3
import hashlib
import os
import random


# DataBase entity
class DB:
    def __init__(self, name):
        self.__name = name
        self.connection = None    #TO DO
        self.cursor = None

    def connect_to_db(self, path_to_db):
        self.connection = sqlite3.connect( os.path.join(path_to_db, self.__name) )
        self.cursor = self.connection.cursor()



# Member entity
class Member(DB):
    def __init__(self, password, ip, plan):
        super(Member, self).__init__('member_info.db')

        self.password = password
        self.member_id = ip.replace('.', '')
        self.plan = plan

    def write_member_data(self):
        sql_command = 'CREATE TABLE ' + 'm' + self.member_id \
                      + '(userid INTEGER PRIMARY KEY,' \
                      + 'password VARCHAR(30),' \
                      + 'ip VARCHAR(15), plan CHAR(1));'

        self.cursor.execute(sql_command)
        format_str = 'INSERT INTO ' + 'm' + self.member_id \
                     + '(userid, password, ip, plan)' \
                     + 'VALUES (NULL, "{}", "{}", "{}");'

        sql_command = format_str.format(self.password, self.member_id, self.plan)
        self.cursor.execute(sql_command)
        self.connection.commit()

    def get_member_data(self):
        self.cursor.execute("SELECT * FROM member")
        return self.cursor.fetchall()



# Storage entity
class Storage(DB):
    def __init__(self, ID):
        super(Storage, self).__init__('storage.db')
        self.ID = ID

    @staticmethod
    def generate_file_id():
        random_num = str(random.random() * 100000)
        fhash = hashlib.md5(random_num.encode('utf-8'))
        return fhash.hexdigest()

    def file_exists(self, file_id):
        if ('f' + file_id,) in self.list_files():
            return True
        else:
            return False

    def list_files(self):
        self.cursor.execute('SELECT name from '
                            + 'sqlite_master where '
                            + 'type= "table"')
        return self.cursor.fetchall()

    def get_file_security(self, file_id):
        if self.file_exists(file_id):
            self.cursor.execute('SELECT slv from ' + 'f' + file_id)
            return self.cursor.fetchall()[0][0]

    def get_file_passwrod(self, file_id):
        if self.file_exists(file_id):
            self.cursor.execute('SELECT ps from ' + 'f' + file_id)
            return self.cursor.fetchall()[0][0]

    def write_file(self, file, passwrod=None):
        if passwrod:
            if not type(passwrod) == str:
                raise ValueError()
        file_id = Storage.generate_file_id()
        if self.file_exists(file_id):
            raise FileExistsError()

        if passwrod:
            security = 'p'
        else:
            security = 'd'

        sql_command = 'CREATE TABLE ' + 'f' + file_id \
                      + '(id INTEGER PRIMARY KEY, ' \
                      + 'file BLOB NOT NULL, ' \
                      + 'filename TEXT, ' \
                      + 'slv CHAR(1), ps TEXT);'

        self.cursor.execute(sql_command)
        sql_command = 'INSERT INTO ' + 'f' + file_id \
                      + '(file, filename, slv, ps)' \
                      + 'VALUES (?, ?, ?, ?);'

        cluster = (file.read(), file.name, security, passwrod)
        self.cursor.execute(sql_command, cluster)
        self.connection.commit()
