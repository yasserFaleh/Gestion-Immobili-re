class User:

    def __init__(self, email, password, firstname=None, lastname=None, birthday=None ):
        self.lastname = lastname
        self.firstname = firstname
        self.birthday = birthday 
        self.email = email # users are identified by emails 
        self.password = password
    
    
    def __init__(self, result):
        self.email = result[0] 
        self.password =  result[1]
        self.lastname =  result[2]
        self.firstname =  result[3]
        self.birthday =  result[4] 


    def to_json(self,):
        return {"email":self.email,"password":self.password,"lastname":self.lastname,"firstname":self.firstname,"birthday":self.birthday}       