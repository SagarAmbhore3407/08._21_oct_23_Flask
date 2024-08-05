
#4. Create a Flask app with a form that accepts user input and displays it.

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/displayinput", methods=['GET','POST'])
def displayinput():
    if request.method == 'POST':
        name = request.form.get('name')
        user_input = request.form.get('user_input')
        return render_template("result.html",name = name,user_input = user_input)
    return render_template('index.html')
        

if __name__ == '__main__':
    app.run(host='localhost',port=5002,debug=True)
