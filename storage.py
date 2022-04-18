import sql, sqlite3, csv

class Table:
    def __init__(self, database, table):
        self.__database = database
        self.__table = table

    def __execute(self, sql_statement):
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute(sql_statement)
            #conn.close()

    def find(self, item):
        #generalised :<<<<< help
        pass
            
    def insert_one(self, record):
        sql_statement = '''INSERT INTO '''

        self.__execute(sql_statement)

    def import_csv(self, file):
        with open(file, 'r') as f:
            for record in csv.DictReader(f):
                self.insert(record)
                
class Student(Table):
    pass

class Class(Table):
    pass
    
class CCA(Table):
    pass

class Activity(Table):
    pass

class Student_CCA(Table):
    pass

class Student_Activity(Table):
    pass
    