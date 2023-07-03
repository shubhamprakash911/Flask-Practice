
from flask import Flask,render_template

app = Flask(__name__)
app.debug=True


@app.route('/')
def index():
    return render_template('index.html')

@app.route("/h")
def temp():
    return 'temp'

if __name__ == '__main__':
    app.run(debug=True)