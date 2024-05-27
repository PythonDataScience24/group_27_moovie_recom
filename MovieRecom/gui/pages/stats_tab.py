
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

from recommendation_system import RecommendationSystem



class VisualizationBox(BoxLayout):
    """Class used to display liked elements."""
    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(VisualizationBox, self).__init__(**kwargs)

        self.recsys = recsys
        self.figureCanvas = None

    def update_visualization(self):
        figure = self.recsys.get_liked_visualization()
        self.clear_widgets()
        self.figureCanvas = FigureCanvasKivyAgg(figure)
        self.add_widget(self.figureCanvas)


class StatsTab(TabbedPanelItem):
    """Class used to display a search tab."""

    def __init__(self, recsys:RecommendationSystem, **kwargs):
        super(StatsTab, self).__init__(text="Stats")

        self.recsys = recsys

        self.stats_layout = BoxLayout(orientation='horizontal')
        self.visualization = VisualizationBox(self.recsys)

        self.stats_layout.add_widget(self.visualization)

        self.add_widget(self.stats_layout)


    def update(self):
        """Updates the stats tab."""
        # Update the visualization
        self.recsys.update_liked_visualizations()
        self.visualization.update_visualization()
