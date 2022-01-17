from email import message
from flask import Flask,request,abort,make_response,jsonify
from dbmanager import Databasemanager


dbm = Databasemanager()
dbm.init() # connecting to the db

app = Flask(__name__)



@app.route('/api/users/register', methods=['PUT'])
def register():
    if not request.json or not 'email' in request.json or not 'password' in request.json :
        abort(400,' content badly formed ')
    else:
        email = request.json['email']
        password = request.json['password']

        if dbm.checkEmailExisting(email) != None :
            abort(400,'Email already used')
        
        # mail doesn't exist so we can register the requester
        else :
            firstname = None
            lastname = None
            birthday = None
            if 'firstname' in request.json:
                firstname = request.json['firstname'] 
            if 'lastname' in request.json:    
                lastname = request.json['lastname'] 
            if 'birthday' in request.json:    
                birthday = request.json['birthday']
            dbm.register(firstname, lastname, email,password,birthday)

        return jsonify({"response":"registred Succesfuly"})

@app.route('/api/users/update', methods=['POST'])
def updateUser():
    # checking the request body if it contains email and password
    if not request.json or not 'email' in request.json or not 'password' in request.json :
        abort(400,' Missing email and password to check your identity')
    else:
        email = request.json['email']
        password = request.json['password']

        # checking the identity 
        user = dbm.checkUser(email, password)
        
        # if the mail or the password are wrong 
        if user == None :
            abort( 400, 'Email or password is wrong !')

        # if email and password are valid 
        else:
            newmail = user.email
            if 'newmail' in request.json:
                newmail = request.json['newmail']
                if newmail != user.email : 
                    if dbm.checkEmailExisting(newmail) : 
                        abort(400,'The new mail is already used')
                    
                        



            if 'firstname' in request.json:
                user.firstname = request.json['firstname']
            if 'lastname' in request.json:
                user.lastname = request.json['lastname']
            if 'birthday' in request.json:
                user.birthday = request.json['birthday']
            if 'newpassword' in request.json:
                user.password = request.json['newpassword']
            print('user = ' ,user.to_json)
            dbm.updateUser(user,newmail)           
            return jsonify({"response":"updated Succesfuly"})

        
if __name__ == '__main__':
    app.run()
