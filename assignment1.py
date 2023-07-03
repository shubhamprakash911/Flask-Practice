from flask import Flask


app = Flask(__name__)
app.debug=True

@app.route('/')
def welcome():
    return 'welcome, to our flask app'


@app.route('/greet/<username>')
def greet_user(username):
    return f'Hello, {username}'

@app.route('/farewell/<username>')
def farewell_user(username):
    return f'goodbye,{username}'


if __name__=='__main__':
    app.run(debug=True)