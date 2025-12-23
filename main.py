from flask import Flask, render_template, request

app = Flask(__name__)

libri = {"Simone Carassale": {"La Grammatica del Graphic Design": ["74"], "Steve Jobs: una biografia illustrata": ["94"]}}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home', methods=['POST'])
def verify_user():
    name = request.form['name']

    return render_template('index.html', name=name, libri=libri)

app.run(debug=True)