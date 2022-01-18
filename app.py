from flask import Flask,request,abort,jsonify
from dbmanager import Databasemanager
from models.asset import Asset
from models.piece import Piece


dbm = Databasemanager()
dbm.init() # connecting to the db

app = Flask(__name__)


"""
    register user by :
        email : required 
        password : required 
        lastname  : not required
        firstname : not required 
        birthday : not required
    
    exemple of the body request:
        {
            "email":"yasser@gmail.com",
            "password":"password",
            "firstname":"Yasser",
            "lastname":"Faleh"
        } 
""" 
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



"""
    register user by :
        email : required 
        password : required 
        lastname  : not required
        firstname : not required 
        birthday : not required
        newmail : not required
        newpassword : not required
    
    exemple of the body request:
        {
            "email":"yasser@gmail.com",
            "password":"password",
            "firstname":"Yasser",
            "lastname":"Faleh",
            "newpassword":"password1",
            "newmail":"yasser1@gmail.com"
        } 
""" 
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



"""
modify a Asset
    The request body must contains:
      - the email and the password to identified the user 
      - asset json object containing : 
        - name ( not required ) 
        - description ( not required )
        - type ( not required )
        - city ( not required )
        - pieces ( json array object and  not required ) containing :
            - size ( required if the piece object is given )
            - id ( required to modify an existing one else add a new piece)
        EXAMPLE: ------------------------------
        Request body :

        {
        "email":"yasser@gmail.com",
        "password":"password",
        "asset":{
                "id":9,
                "name":"appartement321",
                "description":"cool2",
                "type":"T2",
                "city":"Saint",
                "pieces":[
                    {"id":55,"size":42},
                    {"id":56,"size":22},
                    {"size":33}
                        ]
                }
        }
"""
@app.route('/api/assets/modify', methods=['POST'])
def modifyAsset():
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
            abort(400,'missing asset field in your json')
        asset = request.json['asset']
        if not 'id' in asset:
            abort(400,'missing the asset id field in your json')
        asset_id = asset['id']

        #finding the asset in the db
        asset_object = dbm.findAsset(asset_id)
            
            
        if asset_object == None:
            abort(400,'Asset not found')
        
        if asset_object.emailowner != email :
            abort(400,'Access to modify the asset denied')
        print(asset_object.to_json())
        

        if 'name' in asset:
            asset_object.name = asset['name']
        if 'description' in asset:
            asset_object.description = asset['description']
        if 'type' in asset:
            asset_object.type = asset['type']
        if 'city' in asset:
            asset_object.city = asset['city']
        
        if 'pieces' in asset:
            for piece in asset['pieces']:
                if 'size' not in piece:
                    abort( 400, 'Missing size for a Piece definition')
                if ( not 'id' in piece ) or ( piece['id'] == None ) :
                    asset_object.pieces.append( Piece(size=piece['size'] ) )
                else: 
                    piece_object = asset_object.findPieceById(piece['id'])
                    if piece_object == None : 
                        abort( 400 , 'The Piece with id  '+ str(piece['id']) + ' doesn\'t exist in the asset' )
                    else: 
                        piece_object.size = piece['size']

        dbm.modifyAsset(asset_object)
        return jsonify({"response":"Asset modified Succesfuly"})            



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
# if a request param is given in the request named `city' so the 
#   research is by city given else it returns all assets ( limited to 50 )
@app.route('/api/assets/search', methods=['GET'])
def searchAssetByCity():
    city = request.args.get('city', default = 'all', type = str)
    result = dbm.findByCity(city)
    result_json = [asset.to_json() for asset in result]
    return jsonify(result_json)


if __name__ == '__main__':
    app.run()
