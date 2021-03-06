import json
from typing import NamedTuple, List

import plotly

import plotly.graph_objects as go
from plotly.subplots import make_subplots


class LinePlotInput(NamedTuple):
    x: List
    y: List
    name: str
    secondary_y: bool


class CustomPlot:

    def git_fig(self):
        pass

    def graph_json(self) -> json:
        return json.dumps(self.get_fig(), cls=plotly.utils.PlotlyJSONEncoder)


class GaugePlot(CustomPlot):

    def __init__(self, name, value, delta, gauge, step1, step2, threshold):
        self.name = name
        self.value = value
        self.delta = delta
        self.gauge = gauge
        self.step1 = step1
        self.step2 = step2
        self.threshold = threshold

    def get_fig(self) -> go.Figure:

        fig = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=self.value,
            mode="gauge+number+delta",
            title={'text':  self.name},
            delta={'reference': self.delta},
            gauge={'axis': {'range': [None, self.gauge]},
                   'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, self.step1], 'color': "lightgray"},
                        {'range': [self.step1, self.step2], 'color': "gray"}],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': self.threshold}}))

        return fig

    def __repr__(self) -> str:
        return f"GaugePlot({self.name=}, {self.value=}," \
               f" {self.delta=}, {self.gauge=}," \
               f" {self.step1=}, {self.step2=}," \
               f" {self.threshold}"


class LinePlot(CustomPlot):

    def __init__(self):
        self.lineplots = []

    def add(self, lineplot: LinePlotInput):
        self.lineplots.append(lineplot)

    def get_fig(self) -> go.Figure:
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        if self.lineplots:
            for data in self.lineplots:
                fig.add_trace(go.Scatter(
                    x=data.x,
                    y=data.y,
                    name=data.name), secondary_y=data.secondary_y)

        return fig

    def __repr__(self) -> str:
        return f"LinePlot({self.lineplots=})"
