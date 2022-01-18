from flask import Flask,request,abort,make_response,jsonify
from dbmanager import Databasemanager
from models.asset import Asset
from models.piece import Piece


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

@app.route('/api/assets/modify', methods=['POST'])
def modifyAsset():
    pass

""" 
    creates a Asset
    The request body must contains:
      - the email and the password to identified the user
      - asset json object containing : 
        - name ( not required ) 
        - description ( not required )
        - type ( not required )
        - city ( not required )
        - pieces ( json array object and  not required ) containing :
            - size ( required )

        EXAMPLE: ------------------------------
        Request body :
        {
        "email":"yasser@gmail.com",
        "password":"password",
        "asset":{
                "name":"appartement32",
                "description":"cool",
                "type":"T1",
                "city":"Paris",
                "pieces":[
                    {"size":40},
                    {"size":20},
                    {"size":30}
                        ]
                }
        }
"""
@app.route('/api/assets/create', methods=['PUT'])
def createAsset():
    #checking identity
    if not request.json or not 'email' in request.json or not 'password' in request.json :
        abort(400,' Missing email and password to check your identity')
    
    email = request.json['email']
    password = request.json['password']

    # checking the identity 
    user = dbm.checkUser(email, password)

    # if the mail or the password are wrong 
    if user == None :
        abort( 400, 'Email or password is wrong !')

    # if email and password are valid 
    else:
        if not 'asset' in request.json:
            abort(400,'missing asset field to your json')
        asset = request.json['asset']
        name = None
        description = None
        type = None
        city = None
        pieces = []
        if 'name' in asset:
            name = asset['name']
        if 'description' in asset:
            user.description = asset['description']
        if 'type' in asset:
            type = asset['type']
        if 'city' in asset:
            city = asset['city']
        
        if 'pieces' in asset:
            for piece in asset['pieces']:
                if 'size' not in piece:
                    abort( 400, 'Missing size for a Piece definition')
                pieces.append( Piece(size=piece['size'] ) )
        
        dbm.addAsset(Asset(name=name,description=description,type=type,city=city,emailowner=email,pieces=pieces))
        return jsonify({"response":"Asset created Succesfuly"})

# serching by cities         
@app.route('/api/assests/search', methods=['GET'])
def searchAssetByCity():
    city = request.args.get('city', default = 'all', type = str)
    result = dbm.findByCity(city)
    result_json = [asset.to_json() for asset in result]
    return jsonify(result_json)


if __name__ == '__main__':
    app.run()
