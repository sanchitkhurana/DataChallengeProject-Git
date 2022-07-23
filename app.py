from flask import Flask ,render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Searchbooks')
def searchbooks():
    return render_template('spselection.html')

@app.route("/Topfiftybooks")
def topfiftybooks():
    return render_template('topbooks.html')

if __name__ == "__main__":
    app.run(debug=True)