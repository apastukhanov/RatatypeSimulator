import json

import pandas as pd
from flask import Flask, render_template


from calculator import Calculator
from plotutils import *
from user import User


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
    
    df0 = df.copy()
    df0['timestamp'] = pd.to_datetime(df0['timestamp'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%d %B %Y, %H:%M')
    
    df1 = df0.sort_values(by='timestamp', ascending=False).reset_index().drop('index', axis=1).head(7)
    df2 = df0.groupby(by="language")[['speed', 'accuracy']].mean()

    fig1 = Gauge(name='speed', value=df2.loc['en', 'speed'],
                 delta=350, gauge=350, step1=250, step2=400, threshold=490)

    fig2 = Gauge(name='accuracy', value=df2.loc['en', 'accuracy'],
                 delta=94, gauge=100, step1=90, step2=100, threshold=95)

    fig3 = Gauge(name='speed', value=df2.loc['ru', 'speed'],
                 delta=350, gauge=500, step1=250, step2=400, threshold=490)

    fig4 = Gauge(name='accuracy', value=df2.loc['ru', 'accuracy'],
                 delta=94, gauge=100, step1=90, step2=100, threshold=95)

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    df['timestamp'] = df['timestamp'].dt.strftime('%d.%m.%Y')

    en = df.loc[(df['language'] == 'en') & (df['user'] == user.get_user())].groupby(by=['timestamp'])[
        ['speed', 'accuracy']].mean()

    ru = df.loc[(df['language'] == 'ru') & (df['user'] == user.get_user())].groupby(by=['timestamp'])[
        ['speed', 'accuracy']].mean()

    ln_plt = LinePlot()

    ln_plt.add(LinePlotInput(x=en.index, y=en['accuracy'].values, name='accuracy EN', secondary_y=True))
    ln_plt.add(LinePlotInput(x=en.index, y=en['speed'].values, name='speed EN', secondary_y=False))
    ln_plt.add(LinePlotInput(x=ru.index, y=ru['accuracy'].values, name='accuracy RU', secondary_y=True))
    ln_plt.add(LinePlotInput(x=ru.index, y=ru['speed'].values, name='speed RU', secondary_y=False))

    graphJSON1 = fig1.graph_json()
    graphJSON2 = fig2.graph_json()
    graphJSON3 = fig3.graph_json()
    graphJSON4 = fig4.graph_json()
    graphJSON5 = ln_plt.graph_json()

    return render_template('statistics.html',
                           tables1=[df1.to_html(classes='data', header="true", index=False)],
                           graphJSON1=graphJSON1,
                           graphJSON2=graphJSON2,
                           graphJSON3=graphJSON3,
                           graphJSON4=graphJSON4,
                           graphJSON5=graphJSON5)


def start_server():
    app.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    start_server()
