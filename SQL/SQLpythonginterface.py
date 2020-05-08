# -*- coding: utf-8 -*-
"""
Created on Fri May  8 12:19:49 2020

@author: malyr
"""

import sqlite3 

#SQL interfacing through python


class SQLpyclass:
    def __init__(self, database = "myTable.db"):
        self.database = database
        self.DBcontent = []
        self.DBtables = []
        
        self.fetch_all_tables()
        
    
    def execute(self, sql_command):
        connection = sqlite3.connect(self.database) 
        crsr = connection.cursor() 
          
        crsr.execute(sql_command)  
          
        connection.close()      

    def fetch_all_tables(self):
        connection = sqlite3.connect(self.database) 
        cursor = connection.cursor() 
          
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")  
          
        ans = cursor.fetchall()  
        connection.close()
        tables = []
        for X in ans:
            tables.append(X[0])
        
        self.DBtables = tables
        return tables    

    def fetch_all_entries(self, table = self.table[0]):

        connection = sqlite3.connect(self.database) 
        crsr = connection.cursor() 
          
        # execute the command to fetch all the data from the table emp 
        crsr.execute("SELECT * FROM " + table)  
          
        ans = crsr.fetchall()  
        connection.close() 
        
        self.DBcontent = ans
        return ans
        
    
 




sql = SQLpyclass()
sql.execute("""CREATE TABLE emp (  
                staff_number INTEGER PRIMARY KEY,  
                fname VARCHAR(20),  
                lname VARCHAR(30),  
                gender CHAR(1),  
                joining DATE);""")

sql.execute("""CREATE TABLE mytable2 (  
                staff_number INTEGER PRIMARY KEY,  
                fname VARCHAR(20),  
                lname VARCHAR(30),  
                gender CHAR(1),  
                joining DATE);""")

sql.execute("""INSERT INTO emp VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");""")
sql.execute("""INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");""")

print(sql.fetch_all_tables())

# importing module 
#
#  
## connecting to the database  
#connection = sqlite3.connect("myTable.db") 
#  
## cursor  
#crsr = connection.cursor() 
  
# SQL command to create a table in the database 
#sql_command = """CREATE TABLE emp (  
#staff_number INTEGER PRIMARY KEY,  
#fname VARCHAR(20),  
#lname VARCHAR(30),  
#gender CHAR(1),  
#joining DATE);"""
#  
## execute the statement 
#crsr.execute(sql_command) 
#  
## SQL command to insert the data in the table 
#sql_command = """INSERT INTO emp VALUES (23, "Rishabh", "Bansal", "M", "2014-03-28");"""
#crsr.execute(sql_command) 
#  
## another SQL command to insert the data in the table 
#sql_command = """INSERT INTO emp VALUES (1, "Bill", "Gates", "M", "1980-10-28");"""
#crsr.execute(sql_command) 
#  
## To save the changes in the files. Never skip this.  
## If we skip this, nothing will be saved in the database. 
#connection.commit() 
#  
## close the connection 
#connection.close() 




  
