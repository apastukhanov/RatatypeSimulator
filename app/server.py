from flask import Flask, render_template

from calculator import Calculator


app = Flask(__name__)


@app.route("/start")
def start():
    return "<h1> Redirect to the start page...</h1>"


@app.route("/mytest")
def test():
    return "<h1> Redirect to the start page...</h1>"


@app.route("/openfiledialog/<action>")
def open_file_dialog(action):
    if action == "import":
        return "<h1> Importing data...</h1>"
    if action == "export":
        return "<h1> Exporting data...</h1>"
    if action == "delete":
        return "<h1> Deleting data...</h1>"


@app.route("/statistics")
def statistics():
    table1 = Calculator.get_last_entries_html()
    graphJSON1, graphJSON2, graphJSON3, \
        graphJSON4, graphJSON5 = Calculator.get_graphs_json()

    return render_template('statistics.html',
                           tables1=table1,
                           graphJSON1=graphJSON1,
                           graphJSON2=graphJSON2,
                           graphJSON3=graphJSON3,
                           graphJSON4=graphJSON4,
                           graphJSON5=graphJSON5)


def start_server():
    app.run(host="0.0.0.0", port=80)


if __name__ == "__main__":
    start_server()
