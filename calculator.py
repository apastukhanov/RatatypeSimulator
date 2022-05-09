from datetime import datetime

import os

import pandas as pd


class Calculator:
    PATH_TO_DATA = "data/results.csv"

    def __init__(self, speed, accuracy, lang):
        self.speed = speed
        self.accuracy = accuracy
        self.lang = lang
        self.timestamp = datetime.now()

    def __repr__(self):
        speed = self.speed
        accuracy = self.accuracy
        lang = self.lang
        return f"Calculator ({speed=}, {accuracy=}, {lang=})"

    def save_data(self):
        if os.path.exists(self.PATH_TO_DATA):
            df = pd.read_csv(self.PATH_TO_DATA)
        else:
            df = pd.DataFrame(columns=["timestamp", "speed", "accuracy", "language"])
        df = pd.concat([df, pd.DataFrame(columns=["timestamp", "speed", "accuracy", "language"],
                                         data=[{"timestamp": self.timestamp,
                                                "speed": int(self.speed),
                                                "accuracy": float(self.accuracy.replace(",", ".")),
                                                "language": self.lang}])],
                       ignore_index=True)
        df.to_csv('data/results.csv', mode='w', index=False)

    @classmethod
    def read_data(cls):
        if os.path.exists(cls.PATH_TO_DATA):
            df = pd.read_csv(cls.PATH_TO_DATA)
            return df
        return pd.DataFrame(columns=["timestamp", "speed", "accuracy"])
