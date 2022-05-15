import os.path
from datetime import datetime

import pandas as pd

from settings import *


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
    def read_data(cls):
        if os.path.exists(PATH_TO_PICKLE):
            df = pd.read_pickle(PATH_TO_PICKLE)
            return df
        return pd.DataFrame(columns=cls.COLS)

    @classmethod
    def write_to_csv(cls, path):
        df = cls.read_data()
        if os.path.exists(path):
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

