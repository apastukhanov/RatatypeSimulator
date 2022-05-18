import os.path
from datetime import datetime

import pandas as pd

from settings import *
from user import User
from plotutils import GaugePlot, LinePlot, LinePlotInput


class Calculator:
    COLS = ["timestamp", "speed", "accuracy", "language", "user"]

    def __init__(self, speed, accuracy, lang, user):
        self.speed = speed
        self.accuracy = accuracy
        self.lang = lang
        self.user = user
        self.timestamp = datetime.now()

    def __repr__(self):
        speed = self.speed
        accuracy = self.accuracy
        lang = self.lang
        user = self.user
        return f"Calculator ({speed=}, {accuracy=}, {lang=}, {user=})"

    def save_data(self):
        if os.path.exists(PATH_TO_PICKLE):
            df = pd.read_pickle(PATH_TO_PICKLE)
        else:
            df = pd.DataFrame(columns=self.COLS)
        df = pd.concat([df, pd.DataFrame(columns=self.COLS,
                                         data=[{"timestamp": self.timestamp,
                                                "speed": int(self.speed),
                                                "accuracy": float(self.accuracy.replace(",", ".")),
                                                "language": self.lang,
                                                "user": self.user}])],
                       ignore_index=True)
        df.to_pickle(PATH_TO_PICKLE)

    @classmethod
    def read_data(cls, user=None):
        if os.path.exists(PATH_TO_PICKLE):
            df = pd.read_pickle(PATH_TO_PICKLE)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y-%m-%d %H:%M:%S.%f')
            if user:
                return df.loc[df["user"] == user]
            return df
        return pd.DataFrame(columns=cls.COLS)

    @classmethod
    def write_to_csv(cls, path):
        df = cls.read_data()
        if path.split('.')[-1] != 'csv':
            path = path + '.csv'
        if os.path.exists(os.path.dirname(path)):
            df.to_csv(path, index=False)
            return True
        return False

    @classmethod
    def import_data_from_csv(cls, path):
        if not path.split('.')[-1] == "csv":
            return False
        df = pd.read_csv(path)
        if list(df.columns) != list(cls.COLS):
            return False
        df.to_pickle(PATH_TO_PICKLE)
        return True

    @classmethod
    def get_last_entries_html(cls):
        user = User().get_user()
        df = cls.read_data(user)
        df['timestamp'] = df['timestamp'].dt.strftime('%d %B %Y, %H:%M')
        df = df.sort_values(by='timestamp',
                            ascending=False).reset_index().drop('index',
                                                                axis=1).head(7)
        return [df.to_html(classes='data', header="true", index=False)]

    @classmethod
    def get_graphs_json(cls):
        user = User().get_user()
        df = cls.read_data(user)
        df0 = df.groupby(by="language")[['speed', 'accuracy']].mean()

        fig1 = GaugePlot(name='speed', value=df0.loc['en', 'speed'],
                         delta=350, gauge=500, step1=300, step2=500, threshold=400)
        fig2 = GaugePlot(name='accuracy', value=df0.loc['en', 'accuracy'],
                         delta=95, gauge=100, step1=90, step2=100, threshold=95)
        fig3 = GaugePlot(name='speed', value=df0.loc['ru', 'speed'],
                         delta=350, gauge=500, step1=300, step2=500, threshold=400)
        fig4 = GaugePlot(name='accuracy', value=df0.loc['ru', 'accuracy'],
                         delta=95, gauge=100, step1=90, step2=100, threshold=95)
        fig5 = cls.get_line_plot_fig(df)

        figs = [fig1, fig2, fig3, fig4, fig5]
        figs_json = []
        for f in figs:
            figs_json.append(f.graph_json())

        return figs_json

    @classmethod
    def get_line_plot_fig(cls, df):
        df['timestamp'] = df['timestamp'].dt.strftime('%d.%m.%Y')

        en = df.loc[(df['language'] == 'en')].groupby(
            by=['timestamp'])[['speed', 'accuracy']].mean()
        ru = df.loc[(df['language'] == 'ru')].groupby(
            by=['timestamp'])[['speed', 'accuracy']].mean()

        ln_plt = LinePlot()
        ln_plt.add(LinePlotInput(x=en.index, y=en['accuracy'].values,
                                 name='accuracy EN', secondary_y=True))
        ln_plt.add(LinePlotInput(x=en.index, y=en['speed'].values,
                                 name='speed EN', secondary_y=False))
        ln_plt.add(LinePlotInput(x=ru.index, y=ru['accuracy'].values,
                                 name='accuracy RU', secondary_y=True))
        ln_plt.add(LinePlotInput(x=ru.index, y=ru['speed'].values,
                                 name='speed RU', secondary_y=False))
        return ln_plt


