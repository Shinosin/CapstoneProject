import sql, sqlite3, csv

class Table:
    def __init__(self, database:str, table:str, columns:list) -> None:
        self.__database = database
        self.__table = table
        self.__columns = columns

    def execute(self, sql_statement:str, values=[]) -> None:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            if values == []:
                cur.execute(sql_statement)
            else:
                cur.execute(sql_statement, tuple(values))
            #conn.close()
                
    def import_csv(self, file:str) -> None: 
        with open(file, 'r') as f:
            for record in csv.DictReader(f):
                self.insert(record)

    def find(self, record:dict, column='*') -> list: 
        #generalised code
        sql_statement = 'SELECT ' + column + ' FROM ' + self.__table + ' WHERE'
        
        keys = dict.keys() #column names
        valid_keys = [] #valid columns
        values = []
        
        if column not in self.columns: #verify column in parameter 
            return [] 
            
        for key in keys: #verify keys
            if key in self.columns:
                valid_keys.append(key)

        if valid_keys == []: #keys do not exist in the table
            return []

        for key in valid_keys:
            sql_statement += f' {key} = ? AND'
            values += dict[key].upper()

        sql_statement.strip(' AND')
        sql_statement += ';' 
        
        self.__execute(sql_statement, values)

    def get_all(self) -> list:
        sql_statement = 'SELECT * FROM ' + self.__table
        self.execute(sql_statement)

    def insert_one(self, record:dict, sql:str) -> bool:  
        if self.find(record) == []: #empty list, record not in database
            for key, value in record.items():
                if type(value) == str:
                    record[key] = value.upper()
                    
            sql.execute(sql, record)
            return True #inserted
        else:
            return False #did not insert

    def update(self, record:dict, new_record:dict) -> bool:
        if self.find(record) == False:
            return False #cannot update, record not found
        else:
            pass
                
class Student(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'student', ['id', 'name', 'age', 'year_enrolled', 'graduating_year', 'student_class'])
        super().execute(sql.CREATE_STUDENT)
        super().execute(sql.CREATE_STUDENT_SUBJECT)
        super().execute(sql.CREATE_STUDENT_CCA)
        super().execute(sql.CREATE_STUDENT_ACTIVITY)

    def insert(self, record:dict) -> bool:
        super().insert_one(record, sql.INSERT_STUDENT)

class Class(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'class', ['id', 'name', 'level'])

    def insert(self, record:dict) -> bool:
        super().insert_one(record, sql.INSERT_CLASS)    
    
class CCA(Table):
    
    def __init__(self, database:str) -> None:
        super().__init__(database, 'cca', ['id', 'name'])
        
    def insert(self, record:dict) -> bool:
        super().insert_one(record, sql.INSERT_CCA)

class Activity(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'activity', ['id', 'name', 'start_date', 'end_date'])

    def insert(self, record:dict) -> bool:
        super().insert_one(record, sql.INSERT_ACTIVITY)

database = {
    'students': Student('database.db'), 
    'classes': Class('database.db'),
    'ccas': CCA('database.db'),
    'activities': Activity('database.db')
    }