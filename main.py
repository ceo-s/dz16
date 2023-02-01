from flask import Flask, render_template, request
import json
import os
from parse import Parser

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/result/")
def result():
    data = {}
    for dr in os.listdir("static/results"):
        with open(f'static/results/{dr}', 'r') as file:
            data[dr.split('.')[0]] = json.load(file)
    return render_template('result.html', data=data)

@app.route("/settings/", methods=['GET'])
def settings():
    return render_template('settings.html', photo="/static/assets/img/about.jpg")

@app.route("/settings/", methods=['POST'])
def settings_post():
    file = request.form["file"]
    text = request.form["prompt"]
    area = request.form['region']
    print(file, text, area)
    parser = Parser(params={"text": text, "area": area, "professional_role": "96"})
    parser.execute(file_name=file)
    return render_template('settings.html', photo="/static/assets/img/res.jpg")

if __name__ == "__main__":
    app.run(debug=True)