import os, hashlib, sqlite3

# User entity
class Member:

    # User's storage entity
    class Storage:

        # initialize user's storage
        def __init__(self, ip):
            # Encoding user's IP to be hashed and stored as ID
            encoded_ip = ip.encode('utf-8')
            ID = hashlib.md5(encoded_ip)
            # Declaring ID storage field
            self.ID = ID

            # Setting path to DB
            path_to_DB = os.path.join(os.getcwd(), ID.hexdigest(), "storage.db") #TO DO
            # Connecting to storage DB
            self.__connection = sqlite3.connect( path_to_DB )
            self.__cursor = self.__connection.cursor()

        # get user's storage ID
        def get_ID(self):
            return self.ID.hexdigest()

        # write file to user's storage
        def write_file(self, file):
            # Generate fileID
            filename = file.name
            fhash = hashlib.md5(filename.encode('utf-8'))
            fID = fhash.hexdigest()
            # Create table (file)
            sql_command = 'CREATE TABLE ' + 'f' + fID + '(id INTEGER PRIMARY KEY, file BLOB NOT NULL, ' \
                          + 'filename TEXT);'
            self.__cursor.execute(sql_command)

            # Set values of table's items
            sql_command = 'INSERT INTO ' + 'f' + fID + '(file, filename)' \
                         + 'VALUES (?, ?);'
            cluster = ( file.read(), self.get_ID() )
            # Commit changes
            self.__cursor.execute(sql_command, cluster)
            self.__connection.commit()

        # get file from user's storage
        def get_file_data(self, fID):
            self.__cursor.execute("SELECT * FROM " + fID)
            return self.__cursor.fetchall()

        # get all files from user's storage
        def list_files(self):
            self.__cursor.execute('SELECT name from sqlite_master where type= "table"')
            return self.__cursor.fetchall()


    # initialize member
    def __init__(self, password, ip, plan):
        # Initialize entity's fields
        self.__password = password
        self.__ip = ip
        self._plan = plan
        self.storage = self.Storage(ip)
        # Get storage ID and connect to DB
        ID = self.storage.get_ID()
        self.__connection = sqlite3.connect(os.path.join(os.getcwd(), ID, "user_info.db")) #TO DO
        self.__cursor = self.__connection.cursor()

    # write member's data
    def write_member_data(self):
        sql_command = 'CREATE TABLE ' + 'm' + self.storage.get_ID() + '(userid INTEGER PRIMARY KEY, password VARCHAR(30),' \
                      + 'ip VARCHAR(15), plan CHAR(1));'# TO DO
        self.__cursor.execute(sql_command)
        member = [self.__password, self.__ip, self._plan]
        format_str = 'INSERT INTO ' + 'm' + self.storage.get_ID() + '(userid, password, ip, plan)'\
                + 'VALUES (NULL, "{}", "{}", "{}");'
        sql_command = format_str.format(member[0], member[1], member[2]) #TO DO
        self.__cursor.execute(sql_command)
        self.__connection.commit()

    def get_member_data(self):
        self.__cursor.execute("SELECT * FROM member")
        return self.__cursor.fetchall()

    def write_member_file(self, file):
        self.storage.write_file(file)

    def list_member_files(self):
        return self.storage.list_files()

    def get_member_file(self, fID):
        return self.storage.get_file_data(fID)




