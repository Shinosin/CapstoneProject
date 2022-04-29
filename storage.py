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
            
        for key in keys: #verify keys
            if key in self.__columns:
                valid_keys.append(key)

        if valid_keys == []: #keys do not exist in the table
            return []

        for key in valid_keys:
            sql_statement += f' {key} = ? AND'
            if type(record[key]) == str:
                values.append(record[key].upper()) # database values are captitalised
            else:
                values.append(record[key])

        sql_statement = sql_statement.strip(' AND')
        sql_statement += ';' 
        
        return self.execute(sql_statement, values)

    def get_all(self, column='*') -> list:
        sql_statement = 'SELECT ' + column + ' FROM ' + self.__table
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

    # def update(self, record:dict, new_record:dict) -> bool:
    #     if self.find(record) == False:
    #         return False #cannot update, record not found
    #     else: #record found, all columns in record are valid
    #         keys = '' #column(s) to be updated
    #         values = [] #values to be updated
    #         for key1 in record:
    #             for key2 in new_record:
    #                 if key1 == key2: #validate keys in new_record
    #                     keys += key1 + ','
    #                     values += new_record[key2] 
                        
    #         keys = keys.strip(',')
            
    #         sql_statement = 'UPDATE ' + self.__table + ' SET ' 

    #         for key in keys:
    #             sql_statement += f'{key} = ? AND '

    #         sql_statement = sql_statement.strip('AND ')
    #         #idk what exactly this function takes in so um ...
    #         #also this code only works for tables with id (subject and other tables with two primary keys will not work :D)
    #         sql_statement += f'WHERE {"id"} = {record["id"]};'
            
    #         return self.execute(sql_statement, values)
                
class Student(Table):

    def __init__(self, database:str) -> None:
        super().__init__(database, 'student', ['id', 'name', 'age', 'year_enrolled', 'graduating_year', 'student_class'])
        super().execute(sql.CREATE_STUDENT)
        # super().execute(sql.CREATE_STUDENT_SUBJECT)
        # super().execute(sql.CREATE_STUDENT_CCA)
        # super().execute(sql.CREATE_STUDENT_ACTIVITY)

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
        if self.validate_date(record['start_date']): #validate start_date
            if record['end_date'] != '': #check if end_date exists
                if self.validate_date(record['end_date']): #validate end_date
                    return super().insert_one(record, sql.INSERT_ACTIVITY)
            else:
                return super().insert_one(record, sql.INSERT_ACTIVITY)
        else:
            return False #wrong date format 

    def leap_year(self, year:int) -> bool:
        return (year % 4 == 0)

    def validate_date(self, date: str) -> bool:
        #length, type, format check
        if len(date) != 8 or type(date) != str or not date.isdigit():
            return False
        else:
            year, month, day = int(date[:4]), int(date[4:6]), int(date[6:])
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
                elif not self.leap_year(year) and not (1 <= day <= 28): #no leap year
                    return False
            return True

class Student_Subject(Table):
    def __init__(self, database:str) -> None:
        super().__init__(database, 'student_subject', ['student_id', 'subject_code'])
        super().execute(sql.CREATE_STUDENT_SUBJECT)

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_STUDENT_SUBJECT)

class Student_CCA(Table):
    def __init__(self, database:str) -> None:
        super().__init__(database, 'student_cca', ['student_id', 'cca_id', 'role'])
        super().execute(sql.CREATE_STUDENT_CCA)

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_STUDENT_CCA)

    def delete(self, record:dict) -> bool:
        #record = {'student_id':int, 'cca_id':int}
        if super().find(record) != []: #record is in student_cca
            super().execute(sql.DELETE_STUDENT_CCA, (record['student_id'], record['cca_id'],))
            return True #record deleted
        else: 
            return False #cannot delete, record does not exist

    def update_role(self, record:dict, role:str) -> bool:
        #record = {'student_id':int, 'cca_id':int}
        if super().find(record) != []:
            super().execute(sql.UPDATE_STUDENT_CCA, (role.upper(),record['student_id'],record['cca_id'],))
            return True #record updated
        else:
            return False #cannot update, record does not exist

    def existing_members(self, cca_id:int) -> list:
        return super().execute(sql.IN_CCA, (cca_id,))

    def not_in_cca(self, cca_id:int) -> list:
        return super().execute(sql.NOT_IN_CCA, (cca_id,))

    def add_members(self, student_ids:list, cca_id:int) -> bool:
        '''
        add_members adds members who do not belong in the cca 
        student_ids is a list of students who are not in the cca
        '''
        for student_id in student_ids:
            record = {'student_id':student_id,
                     'cca_id':cca_id,
                     'role':'MEMBER'}
            self.insert(record)

    def select_by_student_id(self, student_ids:list) -> list:
        data = []
        for student_id in student_ids:
            data.extend(self.execute(
                sql.SELECT_BY_STUDENT_ID, (student_id, )
            )
        )
        return data

    def display_membership(self, cca_id:int) -> list:
        return super().execute(sql.DISPLAY_MEMBERSHIP, (cca_id,))
                
class Student_Activity(Table):
    def __init__(self, database:str) -> None:
        super().__init__(database, 'student_activity', ['student_id', 'activity_id', 'category', 'role', 'award', 'hours', 'coordinator']) #coordinator is cca id
        super().execute(sql.CREATE_STUDENT_ACTIVITY)

    def insert(self, record:dict) -> bool:
        return super().insert_one(record, sql.INSERT_STUDENT_ACTIVITY)

    def delete(self, record:dict) -> bool:
        #record = {'student_id':int, 'activity_id':int}
        if super().find(record) != []: #record is in student_activity
            super().execute(sql.DELETE_STUDENT_ACTIVITY, (record['student_id'], record['activity_id'],))
            return True #record deleted
        else: 
            return False #cannot delete, record does not exist

    def update(self, record:dict, new_record:dict) -> bool:
        '''
        record = {'student_id':int, 'activity_id':int}
        new_record is a dictionary that can take in the activity category, role, award, hours, coordinator
        e.g. new_record = {'category':str, 'role':str, 'award':str}
        '''
        if super().find(record) != []:
            sql_statement = 'UPDATE student_activity SET '
            columns_to_update = new_record.keys()
            valid_columns = [] 
            data = [] #data to be updated in valid_columns

            for column in columns_to_update:
                if column in self.__columns:
                    valid_columns.append(column)

            if valid_columns == []:
                return False #cannot update, no valid columns

            for column in valid_columns:
                sql_statement += f' {column} = ? AND '
                if type(new_record[column]) == str:
                    data.append(new_record[column]).upper() #captialise values 
                else:
                    data.append(new_record[column])

            sql_statement = sql_statement.strip('AND ')
            sql_statement += f'WHERE student_id = {record["student_id"]} AND {record["activity_id"]};'
                
            super().execute(sql_statement, data)
            return True #record updated
        else:
            return False #cannot update, record does not exist

    def existing_participants(self, activity_id:int) -> list:
        return super().execute(sql.IN_ACTIVITY, (activity_id,))

    def not_in_activity(self, activity_id:int) -> list:
        return super().execute(sql.NOT_IN_ACTIVITY, (activity_id,))

    def add_participants(self, student_ids:list, activity_id:int) -> bool:
        '''
        add_participants adds participants who are not recorded in the activity yet
        student_ids is a list of students who are not recorded in the activity
        '''
        for student_id in student_ids:
            #WHAT DO CATEGORY, AWARD AND HOURS TAKE IN 
            record = {'student_id':student_id,
                     'activity_id':activity_id,
                     'category':'',
                     'role':'PARTICIPANT',
                     'award':'',
                     'hours':'',
                     'coordinator':''}
            self.insert(record)

    def select_by_student_id(self, student_ids:list) -> list:
        data = []
        for student_id in student_ids:
            data.extend(self.execute(sql.SELECT_BY_STUDENT_ID,(student_id['id'], )))
        return data

    def display_participation(self, activity_id:int) -> list:
        return super().execute(sql.DISPLAY_PARTICIPATION, (activity_id,))
        
database = {
    'students': Student('database.db'), 
    'classes': Class('database.db'),
    'ccas': CCA('database.db'),
    'activities': Activity('database.db'),
    'subjects': Subject('database.db'),
    'student_subject': Student_Subject('databse.db'),
    'student_cca': Student_CCA('database.db'),
    'student_activity': Student_Activity('database.db')
    }

database['students'].import_csv('student.csv')
database['classes'].import_csv('class.csv')
database['ccas'].import_csv('cca.csv')
database['subjects'].import_csv('subject.csv')
database['student_subject'].import_csv('student_subject.csv')
database['student_cca'].import_csv('student_cca.csv')