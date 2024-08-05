
#3. Develop a Flask app that uses URL parameters to display dynamic content

from flask import Flask, request, render_template, redirect,url_for

app = Flask(__name__)

@app.route("/")
def index():
    #name = "sagar"
    return render_template("index.html")

@app.route("/isEligible", methods = ['POST'])
def isEligible():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        email = request.form.get('email')
        
        if int(age) < 18:
            wait = 18 - int(age)
            eligibility = "Non Eligible"
            message = f"Hello {name}..!You are not Eligible for Voting..After {wait} yr You can Vote.. "
        else:
            wait = 0
            eligibility = "Yes. Eligible"
            message = f"Hello {name}..!You are Eligible for Voting..You will receive the Voting Venue on mail : {email} "
               
        dynamic_url = url_for('votingEligibility',name=name, age=age, eligibility=eligibility, wait=wait, email=email, message=message)
        return redirect(dynamic_url)
    
    
@app.route('/votingEligibility/<name>/<age>/<eligibility>/<wait>/<email>/<message>')
def votingEligibility(name,age,eligibility,wait,email,message):
    return f"<h1><u><i>Voting Eligibility Status</i></u></h1><p>Name : {name}</p><p>Age : {age}</p><p>Eligibility_Status: {eligibility}</p><p>Wait for Voting: {wait}yr</p><p>Mail : {email}</p><br><h2>{message}</h2>"
    

if __name__ == "__main__":
    app.run(debug = True,host='localhost',port=8000)