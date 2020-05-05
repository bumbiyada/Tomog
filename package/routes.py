from package import app

from flask import render_template
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/tomograph', methods=['GET'])
def tomograph():
    return render_template('tomograph.html')

@app.route('/manufacture', methods=['GET'])
def manufacture():
    return render_template('manufacture.html')

