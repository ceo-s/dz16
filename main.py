from flask import Flask, render_template, request
from parse import ParserStats, ParserTable
from db.declarative_alchemy import save_request, return_built_info
from static.data import parsed_data_keys as pdk

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('main.html')

@app.route("/result/")
def result():
    
    data = list(return_built_info())
    """for dr in os.listdir("static/results"):
        with open(f'static/results/{dr}', 'r') as file:
            data[dr.split('.')[0]] = json.load(file)"""
    return render_template('result.html', data=data)

@app.route("/settings/", methods=['GET'])
def settings():
    choice = pdk
    return render_template('settings.html', photo="/static/assets/img/about.jpg", choice=choice)

@app.route("/settings/", methods=['POST'])
def settings_post():
    file = request.form['file']
    text = request.form["prompt"]
    area = request.form['region']
    if not all(request.form.values()):
        return render_template('settings.html', photo="/static/assets/img/error.gif")
    params = list(request.form.keys())[3:]
    
    parser = ParserTable(params={"text": text, "area": area})
    save_request(vacancy_name=text, region=area, filename=f"{file}{parser.ext}")
    parser.execute(params=params, file_name=file)
    del parser
    return render_template('settings.html', photo="/static/assets/img/res.jpg")

if __name__ == "__main__":
    app.run(debug=True)