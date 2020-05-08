# -*- coding: utf-8 -*-
"""
Created on Fri May  8 12:19:49 2020

@author: malyr
"""

import sqlite3 
import pandas as pd

#SQL interfacing through python


class SQLpyclass:
    def __init__(self, database = "myTable.db"):
        self.database = database
        #self.DBcontent = []
        self.tables = []
        
        self.fetch_all_tables()
        
    
    def execute(self, sql_command):
        connection = sqlite3.connect(self.database) 
        cursor = connection.cursor() 
         
        try:
            cursor.execute(sql_command)  
        except:
            print("Unable to execute SQL command")
          
        connection.close()      

    def dump_table(self, table_name):
        connection = sqlite3.connect(self.database)
        table = pd.read_sql_query("SELECT * from " + table_name, connection)
        table.to_csv(table_name + '.csv', index_label='index')
        
        connection.close()
        
    def dump_all_tables(self):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            table_name = table_name[0]
            table = pd.read_sql_query("SELECT * from %s" % table_name, connection)
            table.to_csv(table_name + '.csv', index_label='index')
        cursor.close()
        connection.close()

    def fetch_column_names(self, table):
        connection = sqlite3.connect(self.database) 
        cursor = connection.cursor()
        cursor.execute("Select * from " + table)
        column_names = [i[0] for i in cursor.description]
        return column_names

    def fetch_all_tables(self):
        connection = sqlite3.connect(self.database) 
        cursor = connection.cursor() 
          
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
          
        ans = cursor.fetchall()  
        connection.close()
        tables = []
        for table_name in ans:
            tables.append(table_name[0])
        
        self.tables = tables
        return tables    

    def fetch_all_entries(self, table_name):

        connection = sqlite3.connect(self.database) 
        crsr = connection.cursor() 
          
        # execute the command to fetch all the data from the table emp 
        crsr.execute("SELECT * FROM " + table_name)  
          
        ans = crsr.fetchall()  
        connection.close() 
        
        self.DBcontent = ans
        return ans
        
    
 




sql = SQLpyclass()
#sql.execute("""CREATE TABLE emp (  
#                staff_number INTEGER PRIMARY KEY,  
#                fname VARCHAR(20),  
#                lname VARCHAR(30),  
#                gender CHAR(1),  
#                joining DATE);""")
#
#sql.execute("""CREATE TABLE mytable2 (  
#                staff_number INTEGER PRIMARY KEY,  
#                fname VARCHAR(20),  
#                lname VARCHAR(30),  
#                gender CHAR(1),  
#                joining DATE);""")

sql.execute("""INSERT INTO emp VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");""")
sql.execute("""INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");""")

sql.execute("""INSERT INTO mytable VALUES (3, "Hubert", "Bansai", "M", "2013-03-28");""")
sql.execute("""INSERT INTO mytable VALUES (4, "Dark", "Pen", "M", "1960-10-28");""")

print(sql.tables)
print(sql.fetch_column_names(sql.tables[0]))

sql.dump_all_tables()






  