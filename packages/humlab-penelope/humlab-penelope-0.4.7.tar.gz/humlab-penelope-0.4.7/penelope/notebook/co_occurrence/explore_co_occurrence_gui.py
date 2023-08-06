import pandas as pd
from penelope.notebook.word_trends.displayers.display_top_table import TopTokensDisplayer
from penelope.utility import getLogger

from .. import utility as notebook_utility
from .. import word_trends
from ..co_occurrence.display_data import CoOccurrenceTable

logger = getLogger()


class ExploreGUI:
    def __init__(self):
        self.trends_data: word_trends.TrendsData = None
        self.tab_main: notebook_utility.OutputsTabExt = None
        self.trends_gui: word_trends.TrendsGUI = None
        self.gofs_gui: word_trends.GoFsGUI = None
        self.gofs_enabled: bool = False

    def setup(self) -> "ExploreGUI":
        self.tab_main = notebook_utility.OutputsTabExt(
            ["Data", "Trends", "Options", "GoF", "TopTokens"], layout={'width': '98%'}
        )
        self.trends_gui = word_trends.TrendsGUI().setup(displayers=word_trends.DEFAULT_WORD_TREND_DISPLAYERS)
        self.gofs_gui = word_trends.GoFsGUI().setup() if self.gofs_enabled else None

        return self

    def display(self, trends_data: word_trends.TrendsData) -> "ExploreGUI":

        self.trends_data = trends_data

        self.trends_gui.display(trends_data=trends_data)

        if self.gofs_gui:
            self.gofs_gui.display(trends_data=trends_data)

        # self.tab_main.display_fx_result(0, display_grid, trends_data.memory.get('co_occurrences'), clear=True)
        # self.tab_main.display_fx_result(
        #     0, display_table, self.trim_data(trends_data.memory.get('co_occurrences')), clear=True
        # )

        data: pd.DataFrame = trends_data.memory.get('co_occurrences')

        self.tab_main.display_content(
            0,
            CoOccurrenceTable(
                data,
                compute_options=trends_data.compute_options,
            ),
            clear=True,
        )
        self.tab_main.display_as_yaml(2, trends_data.compute_options, clear=True, width='800px', height='600px')

        top_displayer: TopTokensDisplayer = TopTokensDisplayer(corpus=trends_data.corpus).setup()
        self.tab_main.display_content(4, top_displayer.layout(), clear=True)

        return self

    def layout(self) -> notebook_utility.OutputsTabExt:
        layout: notebook_utility.OutputsTabExt = self.tab_main.display_content(
            1, what=self.trends_gui.layout(), clear=True
        )
        if self.gofs_gui:
            layout = layout.display_content(3, self.gofs_gui.layout(), clear=True)
        return layout
