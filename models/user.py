class User:

    def __init__(self, email, password, lastname=None, firstname=None,  birthday=None):
        self.lastname = lastname
        self.firstname = firstname
        self.birthday = birthday
        self.email = email  # users are identified by emails
        self.password = password

   

    def to_json(self,):
        return {"email":self.email,"password":self.password,"lastname":self.lastname,"firstname":self.firstname,"birthday":self.birthday}       
