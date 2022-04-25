import sql
import sqlite3
import csv

class Table:
    def __init__(self, database:str, table:str, columns:list) -> None:
        self.__database = database
        self.__table = table
        self.__columns = columns

    def execute(self, sql_statement:str, values={}) -> list:
        with sqlite3.connect('database.db') as conn:
            conn.row_factory = sqlite3.Row # turns output into dict
            cur = conn.cursor()
            cur.execute(sql_statement, values)

            results = cur.fetchall()
            list_of_dict = []
            for record in results:
                list_of_dict.append(dict(record)) # convert Row object to dict
            return list_of_dict             
            # conn.close()
                
    def import_csv(self, file:str) -> None: 
        with open(file, 'r') as f:
            for record in csv.DictReader(f):
                self.insert(record)

    def find(self, record:dict, column='*') -> list: 
        #generalised code
        sql_statement = 'SELECT ' + column + ' FROM ' + self.__table + ' WHERE'
        
        keys = record.keys() #column names
        valid_keys = [] #valid columns
        values = []
        
        if column != '*' and column not in self.__columns: #verify column in parameter 
            return []
            
        for key in keys: #verify keys
            if key in self.__columns:
                valid_keys.append(key)

        if valid_keys == []: #keys do not exist in the table
            return []

        for key in valid_keys:
            sql_statement += f' {key} = ? AND'
            values.append(record[key].upper()) # database values are captitalised

        sql_statement = sql_statement.strip(' AND')
        sql_statement += ';' 
        return self.execute(sql_statement, values)

    def get_all(self) -> list:
        sql_statement = 'SELECT * FROM ' + self.__table
        return self.execute(sql_statement)

    def insert_one(self, record:dict, sql:str) -> bool:  
        if self.find(record) == []: #empty list, record not in database
            for key, value in record.items():
                if type(value) == str:
                    record[key] = value.upper() # database values are capitalised
                    
            self.execute(sql, record)
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
        return super().insert_one(record, sql.INSERT_STUDENT)

class Class(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'class', ['id', 'name', 'level'])
        super().execute(sql.CREATE_CLASS)

    def find(self, record:dict, column='*') -> list: 
        sql_statement = 'SELECT ' + column + ' FROM "class" WHERE'
        
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
        
        return self.execute(sql_statement, values)

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_CLASS)    
    
class CCA(Table):
    
    def __init__(self, database:str) -> None:
        super().__init__(database, 'cca', ['id', 'name'])
        super().execute(sql.CREATE_CCA)
        
    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_CCA)

class Activity(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'activity', ['id', 'name', 'start_date', 'end_date'])
        super().execute(sql.CREATE_ACTIVITY)

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_ACTIVITY)

database = {
    'students': Student('database.db'), 
    'classes': Class('database.db'),
    'ccas': CCA('database.db'),
    'activities': Activity('database.db')
    }