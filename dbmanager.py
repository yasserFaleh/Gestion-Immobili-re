import queue
import sqlite3 as sl
from tkinter import N

from models.user import User     #embedded database


class Databasemanager:


    def init(self ):
        # creating the database if not created, and connect ( a file )
        try :
            self.con = sl.connect('embeddedDb.db',check_same_thread=False)
            self.createArchi()
        except :
            print("Error initilising the embedded database")
            exit(1)
    
    def createArchi(self):
        try:
            with self.con:
                self.con.execute("""
                    CREATE TABLE USER (
                        email TEXT NOT NULL PRIMARY KEY , 
                        password TEXT,                      
                        lastname TEXT,
                        firstname TEXT,
                        birthday TEXT
                    );
                """)
                print("Table User  created")
        except:
            print("Table User already exists")

        #creating the ASSET table
        try:
            with self.con:
                self.con.execute("""
                    CREATE TABLE ASSET (
                        asset_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        description TEXT,
                        type TEXT,
                        city TEXT,
                        emailOwner TEXT,
                        FOREIGN KEY(emailOwner) REFERENCES USER(email)
                    );
                """)
                print("Table ASSET  created")
        except:
            print("Table ASSET already exists")
        
         #creating the Piece table
        try:
            with self.con:
                self.con.execute("""
                    CREATE TABLE Piece (
                        piece_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        size REAL,
                        asset_id INTEGER,
                        FOREIGN KEY(asset_id) REFERENCES ASSET(asset_id)
                    );
                """)
                print("Table Piece  created")
        except:
            print("Table Piece already exists")


    def checkEmailExisting(self, email):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM USER where email=? ",(email,))
        # tuple containg the result of the query 
        result = cur.fetchone()
        if result == None:
            return None
        else : 
            print(result)
            return  User(result)

    def checkUser(self, email, password):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM USER where email=? and password=? ",(email,password,))
        # tuple containg the result of the query 
        result = cur.fetchone()
        if result == None:
            return None
        else : 
            print(result)
            return  User(result)
        
    # this method suppose that the email doesn't exist so it creates a user 
    def register( self , firstname, lastname, email, password, birthday):
        cur = self.con.cursor()
        query = ''' INSERT INTO USER(firstname, lastname, email, password, birthday)
              VALUES(?,?,?,?,?) '''
        cur.execute(query,(firstname, lastname, email, password,birthday))
        self.con.commit()
        
    def updateUser(self, user,newmail):
        cur = self.con.cursor()
        query = ''' Update  USER set firstname= ? ,lastname=? , email=? , password=? ,  birthday = ?
              WHERE email=?  '''
        cur.execute(query,(user.firstname, user.lastname, newmail, user.password, user.birthday,user.email))
        
        self.con.commit()