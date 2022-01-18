# Environment
For running this project, you need **Python 3** and the **Flask** web Framework.
## Install Flask
    pip install flask

##  Sqlite3 
You don't need to install sqlite3 module. It is included in the standard library (since Python 2.5).


# Running the app 
Make sure you are in the right directory:  

    cd GestionImmobiliere

Run the app ( Make sure that your local port 5000 is not used ): 

    python app.py


# About   

This project is a microservice with an REST API ( with Flask ) in the property managment field that provides the following features:

- A user can modify the characteristics of an asset  
- Possibility for users to modify their personal information
- Possibility to view assets from a particular city
- An owner can only modify the characteristics of his property.


# Database 
The database used in this project is **Sqlite 3**, an embedded database ( you don't need any pre-configuration)

# Micro-services

##  Register
HTTP Method :  **PUT**  
**Url** : 127.0.0.1:5000/api/users/register  
**firstname** , **lastname** and **birthday** are not required

**Request Body Example** : 
```
{  
    "email":"yasser@gmail.com",  
    "password":"password",  
    "firstname":"Yasser",   
    "lastname":"Faleh",
    "birthday":"19/07/1999"
} 
```




##  Update user information
HTTP Method :  **POST**  

**Url** : 127.0.0.1:5000/api/users/update  

**newpassword** , **newmail** , **firstname** , **lastname** and **birthday** are not required

**Request Body Example** : 
```
{  
    "email":"yasser@gmail.com",  
    "password":"password",  
    "firstname":"Yasser",   
    "lastname":"Faleh",
    "birthday":"19/07/1999"
    "newpassword":"password1",
    "newmail":"yasser1@gmail.com"
} 
```


##  Create an Asset
HTTP Method :  **PUT**  

**Url** : 127.0.0.1:5000/api/assets/create 

**name** , **description** , **type** , **city** and **pieces** are not required.

the **size** is required if the piece object is in json array

**Request Body Example** : 
```
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
```

##  Modify an Asset
HTTP Method :  **POST**  

**Url** : 127.0.0.1:5000/api/assets/modify 

**email** , **password** , **asset** , **id** are  required.

the **size** is required if the piece object is in json array

**Request Body Example** : 
```
    {
        "email":"yasser@gmail.com",
        "password":"password",
        "asset":{
                "id":1,
                "name":"appartement32",
                "description":null,
                "type":"T1",
                "city":"Paris",
                "pieces":[
                    {"size":40},
                    {"size":20},
                    {"size":30}
                        ]
                }
     } 
```

##  Search by city 
HTTP Method :  **GET**  

**Url** : 127.0.0.1:5000/api/assets/search?city=cityToSearchWith 

**Request Param** : city is not required but the response will contain all the assets if the parameter city not specified