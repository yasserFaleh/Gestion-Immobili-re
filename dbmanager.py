import sqlite3 as sl
from models.asset import Asset
from models.piece import Piece

from models.user import User     

#Manager of the embedded database

class Databasemanager:


    def init(self ):
        # creating the database if not created, and connect ( a file )
        try :
            self.con = sl.connect('embeddedDb.db',check_same_thread=False)
            self.createArchi()
        except :
            print("Error initilising the embedded database")
            exit(1)
    
    #create the tables at the start if they are not created 
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
                        CONSTRAINT fk_users
                        FOREIGN KEY(emailOwner) REFERENCES USER(email)
                        ON DELETE CASCADE
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
                        CONSTRAINT fk_assets
                        FOREIGN KEY(asset_id) REFERENCES ASSET(asset_id)
                        ON DELETE CASCADE
                    );
                """)
                print("Table Piece  created")
        except:
            print("Table Piece already exists")

    #check mail if it is already used
    def checkEmailExisting(self, email):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM USER where email=? ",(email,))
        # tuple containg the result of the query 
        result = cur.fetchone()
        if result == None:
            return None
        else : 
            print(result)
            return  User(result[0],result[1],result[2],result[3],result[4])

    #check mail and password if they are valid
    def checkUser(self, email, password):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM USER where email=? and password=? ",(email,password,))
        # tuple containg the result of the query 
        result = cur.fetchone()
        print('result ' , result)
        if result == None:
            return None
        else : 
            print(result)
            return  User(result[0],result[1],result[2],result[3],result[4])
        
    # this method suppose that the email doesn't exist so it creates a user 
    def register( self , firstname, lastname, email, password, birthday):
        cur = self.con.cursor()
        query = ''' INSERT INTO USER(firstname, lastname, email, password, birthday)
              VALUES(?,?,?,?,?) '''
        cur.execute(query,(firstname, lastname, email, password,birthday))
        self.con.commit()
        
    # update information of user
    def updateUser(self, user,newmail):
        cur = self.con.cursor()
        query = ''' Update  USER set firstname= ? ,lastname=? , email=? , password=? ,  birthday = ?
              WHERE email=?  '''
        cur.execute(query,(user.firstname, user.lastname, newmail, user.password, user.birthday,user.email))
        
        self.con.commit()

    # add an asset 
    def addAsset(self, asset ):
        sql = ''' INSERT INTO asset(name, description, type, city, emailOwner)
              VALUES(?,?,?,?,?) '''
        cur = self.con.cursor()
        cur.execute(sql, (asset.name, asset.description, asset.type, asset.city, asset.emailowner))
        self.con.commit()
        id = cur.lastrowid
        print("asset added with id = ",id) # printing
        for piece in asset.pieces:
            self.addPiece(piece.size,id)
    
    #   add Piece to the database without checking the existane of 
    #       the asset with id given
    def addPiece(self, size, asset_id):
        sql = ''' INSERT INTO piece(size, asset_id)
              VALUES(?,?) '''
        cur = self.con.cursor()
        cur.execute(sql, (size, asset_id))
        self.con.commit()
        print("piece added with id = ",cur.lastrowid) # printing

    # get asset from the database by city 
    # if city is equal to 'all` it returns the 50 first asset 
    def findByCity(self, city):
        cur = self.con.cursor()
        if city != 'all':
            cur.execute("SELECT * FROM Asset WHERE city=?", (city,))
        else :
            cur.execute("SELECT * FROM Asset limit 50")
    
        rows = cur.fetchall()
        result = []
        for row in rows:            
            result.append(Asset(id=row[0],name=row[1],description=row[2],type=row[3],city=row[4],emailowner=row[5],pieces=self.getPiecesOfAsset(row[0]))) 

        return result
    
    # getting the pieces of an asset
    def getPiecesOfAsset(self, asset_id):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM Piece WHERE asset_id=?", (asset_id,))
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append(Piece(id=row[0],size=row[1],asset_id=asset_id))
        return result

    # finding an asset by id else it returns None
    def findAsset( self, asset_id):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM asset WHERE asset_id=?", (asset_id,))
        row = cur.fetchone()
        if row == None:
            return None
        else:
            return Asset(id=row[0],name=row[1],description=row[2],type=row[3],city=row[4],emailowner=row[5],pieces=self.getPiecesOfAsset(row[0]))

    # modify an existing asset
    def modifyAsset(self, asset_object):
        cur = self.con.cursor()
        query = ''' Update  Asset set name= ? ,description=? , emailowner=? , type=? ,  city = ?
              WHERE asset_id=?  '''
        cur.execute(query,(asset_object.name, asset_object.description, asset_object.emailowner, asset_object.type, asset_object.city,asset_object.id))
        self.con.commit()

        for piece in asset_object.pieces:
            if piece.id == None:
                 self.addPiece(piece.size,asset_object.id)
            else: 
                self.modifyPiece(piece.id,piece.size)

    # modifying an existing Piece
    def modifyPiece(self, id, size):
        cur = self.con.cursor()
        query = ''' Update  Piece set size= ? 
              WHERE piece_id=?  '''
        cur.execute(query,(size,id))
        self.con.commit()