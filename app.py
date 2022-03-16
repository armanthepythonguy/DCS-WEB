from flask import *  
import pyrebase
import uuid
app = Flask(__name__)  

config = {
    "apiKey": "AIzaSyAnypNBqgLFJEAbuZ5jMXyP5iA7pDHvTjE",
  "authDomain": "dsc-web-2ea6e.firebaseapp.com",
  "projectId": "dsc-web-2ea6e",
  "storageBucket": "dsc-web-2ea6e.appspot.com",
  "messagingSenderId": "242279474680",
  "appId": "1:242279474680:web:2a0cfe3633d6d3954be20d",
  "databaseURL" : "https://dsc-web-2ea6e-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/login',methods = ['POST'])  
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            customer = db.child("users").child(user['localId']).get()
            typeofuser = customer.val()["type"]
            sessions = db.child("sessions").child(user['localId']).get()
            if(sessions.val() == None):
                sessions = db.child("sessions").child(user['localId']).set({"active":str(uuid.uuid4())})
                return {"auth":typeofuser}
            else:
                sessions = db.child("sessions").child(user['localId']).remove()
                print("Gt here")
                sessions = db.child("sessions").child(user['localId']).set({"active":str(uuid.uuid4())})
                return {"auth":typeofuser,"msg":"Previous session terminated"}
        except:
            return {"auth" : False, "msg":"Invalid Credentials"}
    else:
        return {"auth":"Something is wrong"}



@app.route('/logout',methods = ['POST'])  
def logout():
    if request.method == 'POST':
        email = request.json['email']
        try:
            users = db.child("users").get()
            users = users.val()
            for i in users:
                foundemail = db.child("users").child(i).get()
                foundemail = foundemail.val()
                if foundemail == email:
                    user = i
            sessions = db.child("sessions").child(i).remove()
            return {"auth":True}
        except:
            return {"auth":False}
            



@app.route('/register', methods=['POST'])  
def addusers():
    if request.method == "POST":
        email = request.json['email']
        password = request.json['password']
        type = request.json['type']
        try:
            user = auth.create_user_with_email_and_password(email,password)
            data = {
                "email":email,
                "type":type
            }
            results = db.child("users").child(user['localId']).set(data)
            return {"auth" : True, "msg":'Thanks for registering with us.'}
        except Exception as e:
            return {"auth" : False, "msg":"Email ID already registered or passowrd is less than 6 characters"}
    else:
        return {"auth":False, "msg":"Something is wrong"}



@app.route('/addmovie', methods=['POST'])  
def addmovie():
    if request.method == 'POST':
        try:
            name = request.json['name']
            desc = request.json['desc']
            data = {
                "name":name,
                "desc":desc,
            }
            results = db.child("movies").child(str(uuid.uuid4())).set(data)
            return {"auth":True}
        except:
            return {"auth":False}



@app.route('/getcomments', methods=['POST'])
def getcomments():
    if request.method == 'POST':
        try:
            movieid = request.json['movieid']
            movie = db.child("movies").child(movieid).get()
            movie = movie.val()
            print(movie)
            comments = []
            for i in movie:
                if i!='name' or i!='desc':
                    comment = db.child("movies").child(movieid).child(i).child('comment').get()
                    comment = comment.val()
                    comments.append(comment)
            return {"comments":comments}
        except:
            return {"auth":False}




@app.route('/addcomment', methods=['POST'])  
def addcomment():
    if request.method == 'POST':
        try:
            email = request.json['email']
            comment = request.json['comment']
            movieid = request.json['movieid']
            users = db.child("users").get()
            users = users.val()
            print(users)
            for i in users:
                foundemail = db.child("users").child(i).child("email").get()
                foundemail = foundemail.val()
                print(foundemail)
                if foundemail == email:
                    user = i
            data = {
                "email":email,
                "comment":comment
            }
            result = db.child("movies").child(movieid).child(user).set(data)
            return {"auth":True}
        except:
            return {"auth":False}


      
@app.route('/updatecomment', methods=['POST'])  
def updatecomment():
    if request.method == 'POST':
        try :
            email = request.json['email']
            comment = request.json['comment']
            movieid = request.json['movieid']
            users = db.child("users").get()
            users = users.val()
            for i in users:
                foundemail = db.child("users").child(i).get()
                foundemail = foundemail.val()
                if foundemail == email:
                    user = i
            data = {
                "email":email,
                "comment":comment
            }
            result = db.child("movies").child(movieid).child(i).update(data)
            return {"auth":True}
        except:
            return {"auth":False}




@app.route('/deletecomment', methods=['POST'])  
def deletecomment():
    if request.method == 'POST':
        try:
            email = request.json['email']
            movieid = request.json['movieid']
            users = db.child("users").get()
            users = users.val()
            for i in users:
                foundemail = db.child("users").child(i).get()
                foundemail = foundemail.val()
                if foundemail == email:
                    user = i
            result = db.child("movies").child(movieid).child(i).remove()
            return {"auth":True}
        except:
            return {"auth":False}



if __name__ == '__main__':  
   app.run(debug = True)  