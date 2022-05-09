from flask import Flask, render_template

from  calculator import Calculator


app = Flask(__name__)


@app.route("/start")
def start():
    return "<h1>Перенаправляю на стартовую страницу...</h1>"


@app.route("/mytest")
def test():
    return "<h1>Перенаправляю на страницу теста...</h1>"

@app.route("/statistics")
def statistics():
    df = Calculator.read_data()
    df1 = df.sort_values(by='timestamp', ascending=False).reset_index().drop('index', axis=1).head()
    df2 = df.groupby(by="language")[['speed', 'accuracy']].mean()

    return render_template('statistics.html',
                           tables1=[df1.to_html(classes='data', header="true")],
                           titles1=df1.columns.values,
                           tables2=[df2.to_html(classes='data', header="true")],
                           titles2=df2.columns.values)

def start_server():
    app.run(host="0.0.0.0", port=80)

