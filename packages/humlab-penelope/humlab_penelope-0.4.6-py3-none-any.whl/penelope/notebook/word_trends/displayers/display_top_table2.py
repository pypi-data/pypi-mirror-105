from typing import Any

import IPython.display

# import perspective
from penelope.corpus.dtm.vectorized_corpus import VectorizedCorpus

from ...ipyaggrid_utility import display_grid
from .interface import ITrendDisplayer


# FIXME #72 Word trends: No data in top tokens displayer
class TopTokensDisplayer(ITrendDisplayer):
    def __init__(self, name: str = "TopTokens"):
        super().__init__(name=name)

    def setup(self, *_, **__):
        return

    def compile(self, *, corpus: VectorizedCorpus, **__) -> Any:
        top_terms = corpus.get_top_terms(category_column='category', n_count=10000, kind='token+count')
        return top_terms

    def plot(self, plot_data: dict, **_):  # pylint: disable=unused-argument

        with self.output:

            # g = perspective.PerspectiveWidget(plot_data)
            g = display_grid(plot_data)
            IPython.display.display(g)
