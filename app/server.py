import json

import pandas as pd
from flask import Flask, render_template

import plotly

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from calculator import Calculator
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
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f').dt.strftime('%d %B %Y, %H:%M')
    df1 = df.sort_values(by='timestamp', ascending=False).reset_index().drop('index', axis=1).head(7)
    df2 = df.groupby(by="language")[['speed', 'accuracy']].mean()

    fig1 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df2.loc['en', 'speed'],
        mode="gauge+number+delta",
        title={'text': "Speed"},
        delta={'reference': 350},
        gauge={'axis': {'range': [None, 500]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 250], 'color': "lightgray"},
                   {'range': [250, 400], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

    fig2 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df2.loc['en', 'accuracy'],
        mode="gauge+number+delta",
        title={'text': "Accuracy"},
        delta={'reference': 94},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 90], 'color': "lightgray"},
                   {'range': [90, 100], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}}))

    fig3 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df2.loc['ru', 'speed'],
        mode="gauge+number+delta",
        title={'text': "Speed"},
        delta={'reference': 350},
        gauge={'axis': {'range': [None, 500]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 250], 'color': "lightgray"},
                   {'range': [250, 400], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))

    fig4 = go.Figure(go.Indicator(
        domain={'x': [0, 1], 'y': [0, 1]},
        value=df2.loc['ru', 'accuracy'],
        mode="gauge+number+delta",
        title={'text': "Accuracy"},
        delta={'reference': 94},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 90], 'color': "lightgray"},
                   {'range': [90, 100], 'color': "gray"}],
               'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 95}}))

    df = Calculator.read_data()
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
    df['timestamp'] = df['timestamp'].dt.strftime('%d.%m.%Y')

    m = df.loc[(df['language'] == 'en') & (df['user'] == user.get_user())].groupby(by=['timestamp'])[
        ['speed', 'accuracy']].mean()

    d = df.loc[(df['language'] == 'ru') & (df['user'] == user.get_user())].groupby(by=['timestamp'])[
        ['speed', 'accuracy']].mean()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=m.index,
        y=m['accuracy'].values,
        mode="lines",
        name="accuracy EN"
    ), secondary_y=True)

    fig.add_trace(go.Scatter(
        x=m.index,
        y=m['speed'].values,
        mode="lines",
        name="speed EN",
    ))

    fig.add_trace(go.Scatter(
        x=d.index,
        y=d['speed'].values,
        mode="lines",
        name="speed RU",
    ))

    fig.add_trace(go.Scatter(
        x=d.index,
        y=d['accuracy'].values,
        mode="lines",
        name="accuracy RU",
    ), secondary_y=True)

    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON5 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('statistics.html',
                           tables1=[df1.to_html(classes='data', header="true", index=False)],
                           titles1=df1.columns.values,
                           tables2=[df2.to_html(classes='data', header="true")],
                           titles2=df2.columns.values,
                           graphJSON1=graphJSON1,
                           graphJSON2=graphJSON2,
                           graphJSON3=graphJSON3,
                           graphJSON4=graphJSON4,
                           graphJSON5=graphJSON5
                           )


def start_server():
    app.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    start_server()
