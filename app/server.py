from flask import Flask, render_template

from calculator import Calculator
from user import User

from settings import *


app = Flask(__name__)


@app.route("/start")
def start():
    return "<h1>Перенаправляю на стартовую страницу...</h1>"


@app.route("/mytest")
def test():
    return "<h1>Перенаправляю на страницу теста...</h1>"


@app.route("/openfiledialog/<action>")
def open_file_dialog(action):
    if action == "import":
        return "<h1> Импортируем данные...</h1>"
    if action == "export":
        return "<h1> Экспортируем данные...</h1>"
    if action == "delete":
        return "<h1> Удаляем данные...</h1>"




@app.route("/statistics")
def statistics():
    user = User()
    df = Calculator.read_data()
    df = df.loc[df["user"] == user.get_user()]
    df1 = df.sort_values(by='timestamp', ascending=False).reset_index().drop('index', axis=1).head(10)
    df2 = df.groupby(by="language")[['speed', 'accuracy']].mean()

    return render_template('statistics.html',
                           tables1=[df1.to_html(classes='data', header="true")],
                           titles1=df1.columns.values,
                           tables2=[df2.to_html(classes='data', header="true")],
                           titles2=df2.columns.values)


def start_server():
    app.run(host="0.0.0.0", port=80)

