
#10. Design a Flask app with proper error handling for 404 and 500 errors.

from  flask import Flask, render_template

app = Flask(__name__)
app.secret_key = 'abcd'

sampleData = {'key1':'value1','key2':'value2'}

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def error404(error):
    return render_template('404.html',error = error), 404

@app.errorhandler(500)
def error500(error):
    return render_template('500.html',error = error),500

@app.route('/trigger500')
def trigger500():
    try:
        data = sampleData['notexist_key']
    except Exception as e:
        return error500(e)
    




if __name__ == '__main__':
    app.run(debug=True)