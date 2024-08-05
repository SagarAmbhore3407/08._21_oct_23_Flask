
#5. Implement user sessions in a Flask app to store and display user-specific data.

from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)

app.secret_key = 'flaskapp'

#dictionary to store user which worked as database... 
users_data = {'Sagar':'saggy123'}


#Homepage or Login page render route
@app.route("/")
def index():
    return render_template("index.html")

#Signup page render route
@app.route("/signup_page")
def signup_page():
    return render_template('signup.html')

#Dynamic or action Login route
@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users_data:
            if users_data[username] == password:
                session['username'] = username
                message1 = f"Successfully logged in and the session has been Started.. "
                message2 = f"i.e. SessionData : {session['username']}"
                return render_template('loggedin.html',message1 = message1,message2 = message2)
            else:
                message1 = f"User '{username}' is a Valid user but the password is Wrong.."
                message2 = f"Try to enter the valid Password.."    
        
        else:
            message1 = f"User '{username}' is not a Registered User.. "
            message2 = f"Try to login with a Valid User Credentials.."   
        return render_template('message.html',message1 = message1,message2 = message2)      
        

#Dynamic or action Signup route        
@app.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')
        
        if pass1 != pass2:
            message1 = f"Passwords are not matching."
            message2 = f"Go to signup page & Try to Enter the same passwords."
        else:
            users_data[name] =  pass1
            message1 = f"Signup Successful...{name}.."
            message2 = f"To start a session, go to login Page by using quick link.. "
        return render_template('message.html',message1 = message1,message2 = message2)

#Dynamic or action Logout route
@app.route("/logout")
def logout():
    message1 = f"{session['username']}..! You have logged Out..."
    message2 = f"And the session has Expired...."
    session.pop('username', None)
    return render_template('message.html',message1 = message1,message2 = message2)

if __name__ == "__main__":
    app.run(debug=True,port=8002)