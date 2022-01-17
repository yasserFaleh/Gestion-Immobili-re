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

    python api.py


# About   

This project is a microservice with an REST API ( with Flask ) in the property managment field that provides the following features:

- A user can modify the characteristics of an asset  
- Possibility for users to modify their personal information
- Possibility to view assets from a particular city
- An owner can only modify the characteristics of his property.


# Database 
The database used in this project is **Sqlite 3**, an embedded database ( you don't need any pre-configuration)