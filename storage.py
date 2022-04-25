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
            return False #record exists in database, cannot insert

    def update(self, record:dict, new_record:dict) -> bool:
        if self.find(record) == False:
            return False #cannot update, record not found
        else: #record found, all columns in record are valid
            keys = '' #column(s) to be updated
            values = [] #values to be updated
            for key1 in record:
                for key2 in new_record:
                    if key1 == key2: #validate keys in new_record
                        keys += key1 + ','
                        values += new_record[key2] 
                        
            keys = keys.strip(',')
            
            sql_statement = 'UPDATE ' + self.__table + ' SET ' 

            for key in keys:
                sql_statement += f'{key} = ? AND '

            sql_statement = sql_statement.strip('AND ')
            #idk what exactly this function takes in so um ...
            #also this code only works for tables with id (subject and other tables with two primary keys will not work :D)
            sql_statement += f'WHERE {"id"} = {record["id"]};'
            
            return self.execute(sql_statement, values)
                
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

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_CLASS)

class Subject(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'subject', ['subject_code', 'name', 'level'])
        super().execute(sql.CREATE_SUBJECT)

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_SUBJECT)
    
class CCA(Table):
    
    def __init__(self, database:str) -> None:
        super().__init__(database, 'cca', ['id', 'name'])
        super().execute(sql.CREATE_CCA)
        
    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_CCA)

class Activity(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'activity', ['id', 'name', 'start_date', 'end_date', 'description'])
        super().execute(sql.CREATE_ACTIVITY)

    def insert(self, record:dict) -> bool:
        if self.validate_year(record['start_date']): #validate start_date
            if record['end_date'] != '': #check if end_date exists
                if self.validate_year(record['end_date']): #validate end_date
                    return super().insert_one(record, sql.INSERT_ACTIVITY)
            else:
                return super().insert_one(record, sql.INSERT_ACTIVITY)
        else:
            return False #wrong date format 

    def leap_year(self, year:int) -> bool:
        return (year % 4 == 0)

    def validate_date(self, date:str) -> bool:
        #length, type, format check
        if len(date) != 8 or type(date) != str or not date.isdigit():
            return False
        else:
            year, month, day = int(date[:4]), int(date[4:6]), int(date[7:])
            
            #format/range check
            if not (1 <= month <= 12): #check range of month
                return False
            if month in (1, 3, 5, 7, 8, 10, 12) and not (1 <= day <= 31): #months with 31st
                return False
            if month in (4, 6, 9, 11) and not (1 <= day <= 30): #months with 30th
                return False
            if month == 2: #february
                if self.leap_year(year) and not (1 <= day <= 29): #leap year
                    return False
                elif not self.leap_year(year) and (1 <= day <= 28): #no leap year
                    return False
            return True
            
database = {
    'students': Student('database.db'), 
    'classes': Class('database.db'),
    'ccas': CCA('database.db'),
    'activities': Activity('database.db'),
    'subjects': Subject('database.db')
    }

database['students'].import_csv('student.csv')
database['classes'].import_csv('class.csv')
database['ccas'].import_csv('cca.csv')
database['subjects'].import_csv('subject.csv')

